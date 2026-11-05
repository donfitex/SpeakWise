import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
test("learner signs up, sets a goal, places, retries a lesson, resumes and sees progress", async ({
  page,
}) => {
  await page.goto("/account");
  await page
    .getByRole("button", { name: "Create account", exact: true })
    .click();
  const username = `pilot-${Date.now()}`;
  await page.getByLabel("Username", { exact: true }).fill(username);
  await page
    .getByLabel("Email", { exact: true })
    .fill(`${username}@example.test`);
  await page
    .getByLabel("Password", { exact: true })
    .fill("Synthetic-pilot-strong!78");
  await page.getByLabel("Display name", { exact: true }).fill("Sample Learner");
  await page.getByRole("checkbox", { name: /16 or older/ }).check();
  await page
    .getByRole("button", { name: "Create account", exact: true })
    .first()
    .click();
  await expect(
    page.getByRole("heading", { name: "Welcome, Sample Learner." }),
  ).toBeVisible();
  await page.getByLabel("Learning goal").selectOption("grammar");
  await page.getByLabel("Starting level").selectOption("A1");
  await page.getByRole("button", { name: "Save preferences" }).click();
  await expect(page.getByRole("status")).toContainText("Preferences saved");
  await page.getByRole("link", { name: /Find a starting level/ }).click();
  await page.getByRole("button", { name: "Start placement" }).click();
  for (const answer of ["Hello", "is", "It is raining", "would"])
    await page.getByRole("button", { name: answer, exact: true }).click();
  await expect(page.getByRole("heading", { name: "Try B1" })).toBeVisible();
  await page.getByRole("link", { name: "Classroom", exact: true }).click();
  await page
    .getByRole("article")
    .filter({ has: page.getByRole("heading", { name: "Everyday sentences" }) })
    .getByRole("button")
    .click();
  await page.getByLabel("Your answer").selectOption("is");
  await page.getByRole("button", { name: "Check my answer" }).click();
  await expect(page.getByRole("status")).toContainText("Try this model");
  await page.getByLabel("Your answer").selectOption("am");
  await page.getByRole("button", { name: "Check my answer" }).click();
  await expect(
    page.getByRole("heading", { name: /Put these words in order/ }),
  ).toBeVisible();
  await page.reload();
  await expect(
    page.getByRole("heading", { name: /Put these words in order/ }),
  ).toBeVisible();
  await page.getByLabel("Your answer").fill("I am learning English");
  await page.getByRole("button", { name: "Check my answer" }).click();
  await expect(
    page.getByRole("heading", { name: "You made room for progress." }),
  ).toBeVisible();
  await page.getByRole("link", { name: "See your next step" }).click();
  await expect(
    page.getByRole("heading", {
      name: "Sample Learner, keep finding your words.",
    }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Grammar", exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Practice history" }),
  ).toBeVisible();
  const audit = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(audit.violations).toEqual([]);
  await page.screenshot({
    path: "test-results/dashboard-desktop.png",
    fullPage: true,
  });
  await page.setViewportSize({ width: 390, height: 844 });
  await expect(page.getByRole("navigation")).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await page.screenshot({
    path: "test-results/dashboard-mobile.png",
    fullPage: true,
  });
  const mobile = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(mobile.violations).toEqual([]);
  await page.getByRole("link", { name: "My account" }).click();
  await page.getByRole("button", { name: "Sign out", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Sign in", exact: true }).first(),
  ).toBeVisible();
});
test("landing page keyboard path and accessibility", async ({ page }) => {
  await page.goto("/");
  await page.keyboard.press("Tab");
  await expect(
    page.getByRole("link", { name: "Skip to content" }),
  ).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.locator("#main")).toBeFocused();
  expect(
    (
      await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
        .analyze()
    ).violations,
  ).toEqual([]);
});
