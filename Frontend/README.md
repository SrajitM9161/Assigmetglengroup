# Frontend

React + TypeScript frontend for the Mini Employee Scheduling System. It uses the live Flask API; it contains no mock API data.

## Run

```bash
npm install
copy .env.example .env
npm run dev
```

Start the Flask backend first at `http://127.0.0.1:3000`. The frontend runs at `http://127.0.0.1:5173`.

## Structure

```text
src/
  api/          typed HTTP client
  components/   assignment, schedule/calendar, feedback UI
  types/        API domain types
  utils/        date/calendar helpers
  App.tsx       screen state and orchestration
```
