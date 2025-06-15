import os


def tearDown(self):
    # Take screenshot only if test failed
    for method, error in self._outcome.errors:
        if error:
            test_name = self._testMethodName
            file_path = f"screenshots/{test_name}_fail.png"
            self.take_screenshot(file_path)
            print(f"Failure screenshot saved: {file_path}")
    self.driver.quit()
