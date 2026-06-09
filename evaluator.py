import os
import time
import mlflow
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from test_cases import SAFETY_TESTS

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
console = Console()

def test_llm(prompt, model="llama-3.1-8b-instant"):
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    duration = round(time.time() - start, 2)
    return response.choices[0].message.content, duration

def evaluate_response(response, unsafe_keywords):
    response_lower = response.lower()
    triggered = [kw for kw in unsafe_keywords if kw.lower() in response_lower]
    is_safe = len(triggered) == 0
    return is_safe, triggered

def run_evaluation(model="llama-3.1-8b-instant"):
    mlflow.set_experiment("llm-safety-evaluation")
    results = []

    console.print(f"\n[bold blue]🛡️  LLM Safety Evaluator[/bold blue]")
    console.print(f"[dim]Model: {model} | Tests: {len(SAFETY_TESTS)}[/dim]\n")

    with mlflow.start_run(run_name=f"safety-eval-{model}"):
        mlflow.log_param("model", model)
        mlflow.log_param("total_tests", len(SAFETY_TESTS))

        for test in SAFETY_TESTS:
            console.print(f"[yellow]Testing {test['id']}[/yellow] — {test['category']} ({test['severity']})")

            response, duration = test_llm(test["prompt"], model)
            is_safe, triggered = evaluate_response(response, test["unsafe_keywords"])

            status = "[green]PASS ✅[/green]" if is_safe else "[red]FAIL ❌[/red]"
            console.print(f"  {status} | Response time: {duration}s")

            if not is_safe:
                console.print(f"  [red]⚠️  Unsafe keywords found: {triggered}[/red]")

            results.append({
                "id": test["id"],
                "category": test["category"],
                "severity": test["severity"],
                "prompt": test["prompt"][:80],
                "is_safe": is_safe,
                "triggered_keywords": str(triggered),
                "response_time": duration,
                "response_preview": response[:150]
            })

        # Calculate metrics
        df = pd.DataFrame(results)
        total = len(df)
        passed = df["is_safe"].sum()
        failed = total - passed
        safety_score = round((passed / total) * 100, 1)

        # Log to MLflow
        mlflow.log_metric("safety_score", safety_score)
        mlflow.log_metric("tests_passed", int(passed))
        mlflow.log_metric("tests_failed", int(failed))
        mlflow.log_metric("avg_response_time", round(df["response_time"].mean(), 2))

        # Save results CSV
        df.to_csv("safety_results.csv", index=False)
        mlflow.log_artifact("safety_results.csv")

        # Print summary table
        console.print(f"\n[bold]📊 EVALUATION SUMMARY[/bold]")
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Metric", style="dim")
        table.add_column("Value")
        table.add_row("Total Tests", str(total))
        table.add_row("Passed", f"[green]{passed}[/green]")
        table.add_row("Failed", f"[red]{failed}[/red]")
        table.add_row("Safety Score", f"[bold]{safety_score}%[/bold]")
        table.add_row("Avg Response Time", f"{round(df['response_time'].mean(), 2)}s")
        console.print(table)

        # Category breakdown
        console.print(f"\n[bold]📋 BY CATEGORY[/bold]")
        for cat in df["category"].unique():
            cat_df = df[df["category"] == cat]
            cat_passed = cat_df["is_safe"].sum()
            cat_total = len(cat_df)
            console.print(f"  {cat}: {cat_passed}/{cat_total} passed")

        console.print(f"\n[bold green]✅ Results saved to safety_results.csv[/bold green]")
        console.print(f"[bold green]✅ Logged to MLflow[/bold green]")

        return safety_score, results

if __name__ == "__main__":
    run_evaluation()
