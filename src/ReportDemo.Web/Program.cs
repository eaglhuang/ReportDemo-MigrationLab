var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => Results.Ok(new
{
    service = "ReportDemo.Web",
    platform = "HTML5 + ASP.NET Core",
    status = "ready",
    evidence = "ADR-018"
}));

app.MapGet("/healthz", () => Results.Ok(new
{
    status = "ok",
    checkedAt = DateTimeOffset.UtcNow
}));

app.Run();
