using ReportDemo.Shared;

namespace ReportDemo.DownloadGateway;

public enum DownloadStatus
{
    Requested,
    Authorized,
    WatermarkPending,
    Hashing,
    Ready,
    Delivered,
    Denied,
    FailedClosed,
    Expired,
    Cancelled
}

public sealed record DownloadRequestContext(
    string DownloadId,
    string PdfId,
    bool HasAuthenticatedUser,
    bool RoleAllowed,
    bool DataScopeAllowed,
    bool MetadataReady,
    bool AuditWritable,
    bool WatermarkReady,
    bool CopyHashRecorded);

public sealed record DownloadDecision(
    DownloadStatus Status,
    string Code,
    bool CanReturnFile,
    AuditEvent AuditEvent);

public sealed class DownloadGatewayDecisionService
{
    public DownloadDecision Evaluate(DownloadRequestContext context)
    {
        ArgumentNullException.ThrowIfNull(context);

        if (!context.HasAuthenticatedUser)
        {
            return Deny(context, "AUTH_REQUIRED");
        }

        if (!context.RoleAllowed)
        {
            return Deny(context, "AUTH_DENIED");
        }

        if (!context.DataScopeAllowed)
        {
            return Deny(context, "SCOPE_DENIED");
        }

        if (!context.MetadataReady)
        {
            return FailClosed(context, "PDF_NOT_READY");
        }

        if (!context.AuditWritable)
        {
            return FailClosed(context, "AUDIT_FAILED");
        }

        if (!context.WatermarkReady)
        {
            return FailClosed(context, "WATERMARK_FAILED");
        }

        if (!context.CopyHashRecorded)
        {
            return FailClosed(context, "HASH_FAILED");
        }

        return new DownloadDecision(
            DownloadStatus.Ready,
            "READY",
            CanReturnFile: true,
            BuildAudit(context, "download.ready"));
    }

    private static DownloadDecision Deny(DownloadRequestContext context, string code)
    {
        return new DownloadDecision(DownloadStatus.Denied, code, CanReturnFile: false, BuildAudit(context, "download.denied"));
    }

    private static DownloadDecision FailClosed(DownloadRequestContext context, string code)
    {
        return new DownloadDecision(DownloadStatus.FailedClosed, code, CanReturnFile: false, BuildAudit(context, "download.failed_closed"));
    }

    private static AuditEvent BuildAudit(DownloadRequestContext context, string eventType)
    {
        return new AuditEvent(
            eventType,
            ActorId: "system",
            CorrelationId: context.DownloadId,
            PayloadHash: $"{context.DownloadId}:{context.PdfId}:{eventType}".GetHashCode().ToString("X"),
            CreatedAt: DateTimeOffset.UtcNow);
    }
}

