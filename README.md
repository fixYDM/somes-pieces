# SoMES Pieces Repository

**Owner**: fixydm  
**Project**: Self-Optimizing Microgrid Energy Scheduler (SoMES)  

## Structure
- `pieces/`: Domino Pieces
- `dependencies/`: Docker and requirements files
- `config.toml`: Repository configuration
- `.github/workflows/`: CI/CD for building Pieces

## Usage
1. Install Domino CLI
2. Run: `domino-pieces publish`

## Pieces Overview
| Piece | Purpose |
|--------|---------|
| FetchSolargisDataPiece | Downloads Solargis data |
| PreprocessSolargisPiece | Cleans & feature engineers |
| TrainXGBoostPiece | Trains XGBoost model |
| RunSolarForecastPiece | Generates daily forecasts |
| EvaluateAndPlotPiece | Validates & visualizes |
| RegisterModelPiece | Versions model in Domino |
| NotifyTeamPiece | Sends alerts |