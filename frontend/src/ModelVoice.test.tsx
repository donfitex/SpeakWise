// @vitest-environment jsdom
import { afterEach, expect, test, vi } from "vitest";
import { cleanup, render, screen, fireEvent } from "@testing-library/react";
import { ModelVoice } from "./ModelVoice";
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
test("remote voices require explicit permission and captions remain available", () => {
  const speak = vi.fn();
  const synthesis = {
    getVoices: () => [
      {
        name: "Online",
        lang: "en-US",
        localService: false,
        voiceURI: "online",
      },
    ],
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    cancel: vi.fn(),
    speak,
  };
  Object.defineProperty(window, "speechSynthesis", {
    configurable: true,
    value: synthesis,
  });
  vi.stubGlobal(
    "SpeechSynthesisUtterance",
    class {
      constructor(public text: string) {}
    },
  );
  render(<ModelVoice text="Hello Alex" />);
  expect(screen.getByText("Hello Alex")).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "Listen to model" }));
  expect(speak).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole("checkbox"));
  fireEvent.click(screen.getByRole("button", { name: "Listen to model" }));
  expect(speak).toHaveBeenCalledTimes(1);
});
