namespace ReportDemo.Shared;

public sealed record OperationResult(bool Succeeded, string Code, string Message)
{
    public static OperationResult Ok(string code = "OK", string message = "ok") => new(true, code, message);

    public static OperationResult Fail(string code, string message) => new(false, code, message);
}

