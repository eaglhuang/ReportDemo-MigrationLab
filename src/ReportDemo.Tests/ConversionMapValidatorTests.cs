using ReportDemo.Documents;

namespace ReportDemo.Tests;

public sealed class ConversionMapValidatorTests
{
    [Fact]
    public void IsComplete_ReturnsTrue_ForTraceableConversionEntry()
    {
        var validator = new ConversionMapValidator();
        var entry = new ConversionMapEntry(
            QutoraComponent: "DocumentsController",
            SourcePath: "open-source-sandbox/qutora-api/Qutora.API/Controllers/DocumentsController.cs",
            Behavior: "document download",
            Disposition: ConversionDisposition.Ported,
            Reason: "covered by new download gateway",
            TargetTaskId: "TASK-RPT-0023");

        Assert.True(validator.IsComplete(entry));
    }
}

