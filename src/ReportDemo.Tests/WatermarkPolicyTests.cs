using ReportDemo.Watermark;

namespace ReportDemo.Tests;

public sealed class WatermarkPolicyTests
{
    [Fact]
    public void IsRenderable_ReturnsFalse_WhenVerificationCodeIsMissing()
    {
        var policy = new WatermarkPolicy();
        var payload = new WatermarkPayload(
            DownloadId: "dl-001",
            UserId: "user-001",
            Department: "audit",
            SourceIp: "127.0.0.1",
            ReportCode: "RPT-001",
            ReportVersion: "v1",
            DownloadedAt: DateTimeOffset.UtcNow,
            VerificationCode: "");

        Assert.False(policy.IsRenderable(payload));
    }
}

