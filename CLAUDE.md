# SC2 AI Agent Project Guide for Claude Code

## Project Overview
This is a comprehensive StarCraft II AI agent project built with Python, featuring a Zerg bot (WickedZergBot) that aims for challenger-level play. The project includes autonomous coding agents, mobile monitoring, real-time bug tracking, and continuous improvement systems.

## Key Components
- **WickedZergBotIntegrated**: Main Zerg AI bot with RL orchestration
- **Mobile App**: React Native Android app for real-time monitoring
- **Autonomous Agents**: Cline-style agents using Vertex AI/Gemini
- **Monitoring Systems**: Real-time bug tracking, building recognition, telemetry
- **Competition Ready**: Monsterbot for AI Arena submissions
- **Continuous Improvement**: Automated optimization loops

## Architecture
The bot uses a Blackboard pattern with Scout, Economy, and Production managers coordinated through an IntelManager.

## Coding Standards
- Use Python 3.9+
- Follow PEP 8 style guidelines
- Use burnysc2 (python-sc2 fork) for SC2 integration
- Implement FSM for state management
- Use Potential Fields for micro-control

## Key Files
- `run.py`: Competition entry point
- `wicked_zerg_bot_integrated.py`: Main bot class
- `scout_manager.py`: Reconnaissance logic
- `economy_manager.py`: Resource management
- `production_manager.py`: Build orders and unit production
- `mobile_app/`: React Native mobile monitoring app

## Common Tasks
- Fix bugs in build orders and micro-management
- Optimize resource allocation algorithms
- Improve scouting and intel gathering
- Enhance mobile dashboard features
- Add new pro-gamer strategies (Serral, Reynor, Dark)

## Dependencies
- burnysc2
- google-cloud-aiplatform (for Vertex AI)
- flask/fastapi (for web backends)
- rich (for terminal UI)
- React Native (for mobile app)

When working on this project, focus on improving AI decision-making, fixing game logic bugs, and enhancing monitoring capabilities. Always test changes in actual SC2 matches.

Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): 2026-01-10 02:38:38
Current User's Login: sun475300-sudo