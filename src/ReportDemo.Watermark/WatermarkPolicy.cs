namespace ReportDemo.Watermark;

public sealed record WatermarkPayload(
    string DownloadId,
    string UserId,
    string Department,
    string SourceIp,
    string ReportCode,
    string ReportVersion,
    DateTimeOffset DownloadedAt,
    string VerificationCode);

public sealed class WatermarkPolicy
{
    public bool IsRenderable(WatermarkPayload payload)
    {
        ArgumentNullException.ThrowIfNull(payload);

        return !string.IsNullOrWhiteSpace(payload.DownloadId)
            && !string.IsNullOrWhiteSpace(payload.UserId)
            && !string.IsNullOrWhiteSpace(payload.Department)
            && !string.IsNullOrWhiteSpace(payload.SourceIp)
            && !string.IsNullOrWhiteSpace(payload.ReportCode)
            && !string.IsNullOrWhiteSpace(payload.ReportVersion)
            && !string.IsNullOrWhiteSpace(payload.VerificationCode);
    }
}

