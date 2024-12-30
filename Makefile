format:
	pdm run black .

run:
	pdm run uvicorn src.main:app --reload
