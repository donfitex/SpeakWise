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

test("stopping a recording creates local preview and releases microphone tracks", async () => {
  const stop = vi.fn();
  const track = { stop };
  Object.defineProperty(navigator, "mediaDevices", {
    configurable: true,
    value: {
      getUserMedia: vi.fn().mockResolvedValue({ getTracks: () => [track] }),
      enumerateDevices: vi.fn().mockResolvedValue([]),
    },
  });
  class FakeRecorder {
    static isTypeSupported() {
      return true;
    }
    state = "inactive";
    mimeType = "audio/webm";
    ondataavailable: ((e: { data: Blob }) => void) | null = null;
    onstop: (() => void) | null = null;
    start() {
      this.state = "recording";
    }
    stop() {
      this.state = "inactive";
      this.ondataavailable?.({ data: new Blob(["synthetic"]) });
      this.onstop?.();
    }
  }
  vi.stubGlobal("MediaRecorder", FakeRecorder);
  URL.createObjectURL = vi.fn().mockReturnValue("blob:synthetic");
  URL.revokeObjectURL = vi.fn();
  const { unmount } = render(<Recorder />);
  fireEvent.click(screen.getByRole("checkbox"));
  fireEvent.click(screen.getByRole("button", { name: "Start recording" }));
  await waitFor(() =>
    expect(screen.getByRole("button", { name: "Stop recording" })).toBeTruthy(),
  );
  fireEvent.click(screen.getByRole("button", { name: "Stop recording" }));
  expect(screen.getByLabelText("Your recording preview")).toBeTruthy();
  expect(stop).toHaveBeenCalledTimes(1);
  expect(URL.createObjectURL).toHaveBeenCalledTimes(1);
  fireEvent.click(screen.getByRole("button", { name: "Discard and retry" }));
  expect(URL.revokeObjectURL).toHaveBeenCalledWith("blob:synthetic");
  expect(screen.queryByLabelText("Your recording preview")).toBeNull();
  unmount();
});
