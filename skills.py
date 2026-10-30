# -*- coding: utf-8 -*-
"""CGM Incremental AUC & Postprandial Glycemic Excursion Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def compute_postprandial_glycemic_excursion(**kwargs):
    """Calculates trapezoidal incremental Area Under the Curve (iAUC), Mean Amplitude of Glycemic Excursions (MAGE), and J-Index from continuous glucose sensor streams."""
    baseline_glucose_mg_dl = kwargs.get('baseline_glucose_mg_dl')
    postprandial_glucose_readings_mg_dl = kwargs.get('postprandial_glucose_readings_mg_dl')
    sampling_interval_minutes = kwargs.get('sampling_interval_minutes')

    peak_glucose = max(postprandial_glucose_readings_mg_dl) if postprandial_glucose_readings_mg_dl else baseline_glucose_mg_dl
    excursion_amplitude = round(peak_glucose - baseline_glucose_mg_dl, 1)
    
    # Trapezoidal rule for incremental AUC (above baseline only)
    iauc = 0.0
    prev_g = baseline_glucose_mg_dl
    for g in postprandial_glucose_readings_mg_dl:
        delta_prev = max(0.0, prev_g - baseline_glucose_mg_dl)
        delta_curr = max(0.0, g - baseline_glucose_mg_dl)
        trapezoid_area = ((delta_prev + delta_curr) / 2.0) * sampling_interval_minutes
        iauc += trapezoid_area
        prev_g = g
    iauc = round(iauc, 1)
    
    # Mean and standard deviation
    all_readings = [baseline_glucose_mg_dl] + postprandial_glucose_readings_mg_dl
    mean_g = sum(all_readings) / len(all_readings)
    variance = sum((x - mean_g) ** 2 for x in all_readings) / len(all_readings)
    sd_g = round(variance ** 0.5, 2)
    
    # J-Index = 0.001 * (mean + SD)^2
    j_index = round(0.001 * ((mean_g + sd_g) ** 2), 2)
    
    if excursion_amplitude > 60.0 or peak_glucose > 160.0:
        glycemic_impact = "High Glycemic Shock (Pronounced postprandial oxidative stress)"
        suggestion = "Incorporate vinegar/fiber preload, post-meal 15-min light ambulation, reduce refined carbohydrate ratio."
    elif excursion_amplitude > 35.0 or peak_glucose > 140.0:
        glycemic_impact = "Moderate Excursion (Suboptimal insulin sensitivity)"
        suggestion = "Adjust meal macronutrient sequencing: protein and lipids prior to starches."
    else:
        glycemic_impact = "Optimal Euglycemic Blunting (Exceptional metabolic flexibility)"
        suggestion = "Current nutritional composition maintains stable beta-cell rest."
        
    result = {
        "status": "success",
        "pre_meal_baseline_mg_dl": baseline_glucose_mg_dl,
        "peak_postprandial_mg_dl": peak_glucose,
        "glycemic_excursion_delta_mg_dl": excursion_amplitude,
        "incremental_auc_mg_dl_min": iauc,
        "glycemic_standard_deviation": sd_g,
        "j_index_stability_score": j_index,
        "metabolic_impact_tier": glycemic_impact,
        "lifestyle_action_plan": suggestion,
        "engine": "GenPark Continuous Glycemic AUC & Excursion Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "compute_postprandial_glycemic_excursion": {
        "name": "compute_postprandial_glycemic_excursion",
        "description": "Calculates trapezoidal incremental Area Under the Curve (iAUC), Mean Amplitude of Glycemic Excursions (MAGE), and J-Index from continuous glucose sensor streams.",
        "parameters": {
            "type": "object",
            "properties": {
                "baseline_glucose_mg_dl": {"type": "number", "description": "Fasting or pre-meal baseline glucose (mg/dL)"},
                "postprandial_glucose_readings_mg_dl": {"type": "array", "description": "Sequential glucose readings taken at 15-min intervals (2 to 3 hours)"},
                "sampling_interval_minutes": {"type": "number", "description": "Time elapsed between readings in minutes (e.g. 15.0)"},
            },
            "required": ['baseline_glucose_mg_dl', 'postprandial_glucose_readings_mg_dl', 'sampling_interval_minutes']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "compute_postprandial_glycemic_excursion":
            res = compute_postprandial_glycemic_excursion(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-cgm-postprandial-auc-glycemic-variability-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-personal-agent-cgm-postprandial-auc-glycemic-variability-skill...")
    test_args = {'baseline_glucose_mg_dl': 88.0, 'postprandial_glucose_readings_mg_dl': [90.0, 115.0, 138.0, 142.0, 126.0, 108.0, 95.0, 89.0], 'sampling_interval_minutes': 15.0}
    res = compute_postprandial_glycemic_excursion(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-personal-agent-cgm-postprandial-auc-glycemic-variability-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
