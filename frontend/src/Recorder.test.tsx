// @vitest-environment jsdom
import { afterEach, expect, test, vi } from "vitest";
import {
  cleanup,
  render,
  screen,
  fireEvent,
  waitFor,
} from "@testing-library/react";
import { Recorder } from "./Recorder";
vi.mock("./api", () => ({ api: vi.fn().mockResolvedValue({ granted: true }) }));
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
test("unsupported recording offers a typed path", () => {
  vi.stubGlobal("MediaRecorder", undefined);
  render(<Recorder />);
  expect(screen.getByRole("status").textContent).toContain("typed answer");
});
test("permission rejection is recoverable and capture requires consent", async () => {
  const getUserMedia = vi
    .fn()
    .mockRejectedValue(new DOMException("Denied", "NotAllowedError"));
  Object.defineProperty(navigator, "mediaDevices", {
    configurable: true,
    value: { getUserMedia },
  });
  vi.stubGlobal("MediaRecorder", class {});
  render(<Recorder />);
  const start = screen.getByRole("button", {
    name: "Start recording",
  }) as HTMLButtonElement;
  expect(start.disabled).toBe(true);
  fireEvent.click(screen.getByRole("checkbox"));
  fireEvent.click(start);
  await waitFor(() =>
    expect(screen.getByRole("alert").textContent).toContain("denied"),
  );
  expect(getUserMedia).toHaveBeenCalledTimes(1);
  expect(start.disabled).toBe(false);
});
