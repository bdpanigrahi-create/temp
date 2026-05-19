"""
Filename: execution_incident_healer.py
Description: End-to-end parallel agent graph architecture using Gemini Enterprise ADK.
"""

import os
from google.adk import Agent, Runner
from google.adk.agents import SequentialAgent, ParallelAgent
from google.adk.tools import McpToolset, VectorStoreConnector
from google.adk.runtime import AgentEngineSandboxCodeExecutor
from sre_fleet.log_reader import read_logs_with_auth

# 1. INITIALIZE INFRASTRUCTURE CONNECTORS (BUILD TIER)
datadog_mcp = McpToolset(server_url="http://localhost:8100/mcp/datadog")
github_mcp = McpToolset(server_url="http://localhost:8105/mcp/github")
runbook_rag_db = VectorStoreConnector(index_name="internal-runbook-vectors")

# 2. INSTANTIATE AGENTS WITH ATTACHED TOOLSETS
triage_agent = Agent(name="Log-Triage-Scraper", model="gemini-2.5-pro", tools=[datadog_mcp, read_logs_with_auth])
compliance_agent = Agent(name="Runbook-Compliance-Auditor", model="gemini-2.5-pro", tools=[runbook_rag_db])
planner_agent = Agent(name="Sandbox-Execution-Planner", model="gemini-2.5-pro")
gatekeeper_agent = Agent(name="Hotfix-Gatekeeper", model="gemini-2.5-flash") # Low latency execution feedback

# 3. CONFIGURE SECURE ISOLATED CODE RUNTIME (SCALE TIER)
# Connect the planner agent directly to our serverless sandboxed environment configured in Part 1.5.
planner_agent.set_code_executor(
    AgentEngineSandboxCodeExecutor(
        runtime_environment="python-3.11", 
        timeout_seconds=240,
        network_egress="VPC_ONLY",
        resource_profile="sre-diagnostics-sandbox"
    )
)

# 4. DESIGN ORCHESTRATION PIPELINE LOGIC GRAPH (BUILD MULTI-AGENT)
# In parallel, collect logs and query historical runbooks before converging at the Sandbox planner.
parallel_phase = ParallelAgent(name="Parallel-Triage-Compliance", agents=[triage_agent, compliance_agent])
fleet_flow = SequentialAgent(name="Fleet-Healer-Flow", agents=[parallel_phase, planner_agent, gatekeeper_agent])

def execute_live_healing_run():
    print("🚀 [SYSTEM ACTIVE] Launching Autonomous SRE Self-Healer Loop...")
    
    # Active production incident payload representing a memory leak crash
    incident_alert_trigger = (
        "INCIDENT ALERT: Microservice 'billing_processor' crashed with out-of-memory "
        "exceptions (OOM) under sustained load. Triage incident INC-9902, "
        "reproduce the issue inside the sandbox, check runbooks for the pre-approved fix, "
        "and generate a safe patch deployment branch."
    )
    
    runner = Runner()
    response = runner.run(fleet_flow, initial_input=incident_alert_trigger)
    
    print("\n" + "="*70)
    print("📊 LIVE TERMINAL DISPLAY: ENTERPRISE SRE TELEMETRY TRACE")
    print("="*70)
    print(response.output)

if __name__ == "__main__":
    execute_live_healing_run()
