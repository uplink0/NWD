import unittest

import devdiag


class RedactionTests(unittest.TestCase):
    def test_bearer_token_is_redacted(self):
        self.assertNotIn("secret-token", devdiag.redact("Authorization: Bearer secret-token"))

    def test_password_is_redacted(self):
        self.assertNotIn("mysecret", devdiag.redact("password=mysecret"))

    def test_output_is_bounded(self):
        self.assertLessEqual(len(devdiag.redact("x" * 9000)), devdiag.MAX_OUTPUT)


class DetectionTests(unittest.TestCase):
    def test_crashloop_is_detected(self):
        findings = devdiag.deterministic_findings([
            {"id": "k8s_pods", "status": "ok", "output": "ns api-123 0/1 CrashLoopBackOff"}
        ])
        self.assertTrue(any("CrashLoopBackOff" in item["title"] for item in findings))

    def test_healthy_pod_has_no_crashloop_finding(self):
        findings = devdiag.deterministic_findings([
            {"id": "k8s_pods", "status": "ok", "output": "ns api-123 1/1 Running"}
        ])
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
