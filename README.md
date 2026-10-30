# CGM Incremental AUC & Postprandial Glycemic Excursion Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `compute_postprandial_glycemic_excursion`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Calculates trapezoidal incremental Area Under the Curve (iAUC), Mean Amplitude of Glycemic Excursions (MAGE), and J-Index from continuous glucose sensor streams.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Personal Agent (Bio / Metabolic Longevity)`

## MCP Tool Specification
### `compute_postprandial_glycemic_excursion`
Parameters:
- `baseline_glucose_mg_dl` (float): Fasting or pre-meal baseline glucose (mg/dL)
- `postprandial_glucose_readings_mg_dl` (list): Sequential glucose readings taken at 15-min intervals (2 to 3 hours)
- `sampling_interval_minutes` (float): Time elapsed between readings in minutes (e.g. 15.0)

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-personal-agent-cgm-postprandial-auc-glycemic-variability-skill": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-cgm-postprandial-auc-glycemic-variability-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
