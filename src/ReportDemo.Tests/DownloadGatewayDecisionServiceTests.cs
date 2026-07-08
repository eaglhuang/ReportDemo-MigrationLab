using ReportDemo.DownloadGateway;

namespace ReportDemo.Tests;

public sealed class DownloadGatewayDecisionServiceTests
{
    [Fact]
    public void Evaluate_ReturnsReady_WhenAllRequiredGatesPass()
    {
        var service = new DownloadGatewayDecisionService();
        var context = new DownloadRequestContext(
            DownloadId: "dl-001",
            PdfId: "pdf-001",
            HasAuthenticatedUser: true,
            RoleAllowed: true,
            DataScopeAllowed: true,
            MetadataReady: true,
            AuditWritable: true,
            WatermarkReady: true,
            CopyHashRecorded: true);

        var result = service.Evaluate(context);

        Assert.Equal(DownloadStatus.Ready, result.Status);
        Assert.True(result.CanReturnFile);
        Assert.Equal("READY", result.Code);
    }

    [Fact]
    public void Evaluate_FailsClosed_WhenAuditIsUnavailable()
    {
        var service = new DownloadGatewayDecisionService();
        var context = new DownloadRequestContext(
            DownloadId: "dl-002",
            PdfId: "pdf-001",
            HasAuthenticatedUser: true,
            RoleAllowed: true,
            DataScopeAllowed: true,
            MetadataReady: true,
            AuditWritable: false,
            WatermarkReady: true,
            CopyHashRecorded: true);

        var result = service.Evaluate(context);

        Assert.Equal(DownloadStatus.FailedClosed, result.Status);
        Assert.False(result.CanReturnFile);
        Assert.Equal("AUDIT_FAILED", result.Code);
    }

    [Fact]
    public void CanTransition_AllowsReadyToExpired()
    {
        Assert.True(DownloadStateMachine.CanTransition(DownloadStatus.Ready, DownloadStatus.Expired));
    }

    [Fact]
    public void CanTransition_BlocksDeliveredToReady()
    {
        Assert.False(DownloadStateMachine.CanTransition(DownloadStatus.Delivered, DownloadStatus.Ready));
    }
}
