import { StrictMode, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Alert, Box, Button, Chip, CssBaseline, Paper, Stack, Typography } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import './styles.css';

const sports = {
  run: { label: 'Run', color: '#c5ee78' },
  trail_run: { label: 'Trail run', color: '#55c9ad' },
  ride: { label: 'Ride', color: '#89b1f8' },
  swim: { label: 'Swim', color: '#78d7e3' },
  strength: { label: 'Strength', color: '#f2ad71' },
  other: { label: 'Other', color: '#c5baf4' },
};

type Sport = keyof typeof sports;
const sportKeys = Object.keys(sports) as Sport[];

type Activity = {
  source_id: number;
  sport: Sport;
  started_at: string;
  moving_seconds: number;
  distance_meters: number | null;
};
type TrainingWeek = {
  week_start: string;
  seconds_by_sport: Partial<Record<Sport, number>>;
  activities: Activity[];
};
type DemoReport = { source: 'synthetic'; timezone: string; weeks: TrainingWeek[] };

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#c5ee78', contrastText: '#111718' },
    background: { default: '#111718', paper: '#192223' },
  },
  typography: { fontFamily: 'system-ui, sans-serif' },
  shape: { borderRadius: 10 },
});

const weekDate = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', timeZone: 'UTC' });
const distanceFormat = new Intl.NumberFormat('en-GB', { maximumFractionDigits: 2 });

function total(week: TrainingWeek) {
  return Object.values(week.seconds_by_sport).reduce((sum, seconds) => sum + seconds, 0);
}

function duration(seconds: number) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainder = seconds % 60;
  const chunks = [hours && `${hours} h`, minutes && `${minutes} min`, remainder && `${remainder} s`];
  return chunks.filter(Boolean).join(' ') || '0 min';
}

function WeekChart({ weeks, selected, onSelect }: {
  weeks: TrainingWeek[];
  selected: string | undefined;
  onSelect: (start: string) => void;
}) {
  const max = Math.max(1, ...weeks.map(total));
  const visibleSports = sportKeys.filter((sport) => weeks.some((week) => sport in week.seconds_by_sport));
  return (
    <Paper component="section" variant="outlined" className="panel" aria-labelledby="weekly-heading">
      <Typography component="h2" variant="h6" id="weekly-heading">Training time by week</Typography>
      <ul className="legend" aria-label="Sports">
        {visibleSports.map((sport) => <li key={sport}><i style={{ background: sports[sport].color }} />{sports[sport].label}</li>)}
      </ul>
      <div className="bar-list">
        {[...weeks].reverse().map((week) => {
          const label = weekDate.format(new Date(week.week_start));
          const sportTotals = visibleSports.flatMap((sport) => {
            const seconds = week.seconds_by_sport[sport];
            return seconds === undefined ? [] : [`${sports[sport].label} ${duration(seconds)}`];
          });
          return (
            <button key={week.week_start} type="button" className="week-bar"
              aria-pressed={selected === week.week_start} aria-controls="sessions"
              aria-label={[`Week of ${label}`, duration(total(week)), ...sportTotals].join(', ')}
              onClick={() => onSelect(week.week_start)}>
              <span>{label}</span>
              <span className="track" aria-hidden="true">
                {visibleSports.map((sport) => <span key={sport} title={sports[sport].label}
                  style={{ width: `${100 * (week.seconds_by_sport[sport] ?? 0) / max}%`, background: sports[sport].color }} />)}
              </span>
              <span>{duration(total(week))}</span>
            </button>
          );
        })}
      </div>
    </Paper>
  );
}

function SessionList({ week, timezone }: { week: TrainingWeek; timezone: string }) {
  const activityDate = new Intl.DateTimeFormat('en-GB', { dateStyle: 'medium', timeStyle: 'short', timeZone: timezone });
  return (
    <Paper component="section" variant="outlined" id="sessions" className="panel" aria-labelledby="session-heading">
      <Typography component="h2" variant="h6" id="session-heading">Week of {weekDate.format(new Date(week.week_start))}</Typography>
      <ul className="session-list">
        {week.activities.map((activity) => (
          <li key={activity.source_id}>
            <div><strong>{sports[activity.sport].label}</strong><br />
              <time dateTime={activity.started_at}>{activityDate.format(new Date(activity.started_at))}</time></div>
            <div><strong>{duration(activity.moving_seconds)}</strong><br />
              {activity.distance_meters === null ? 'No distance' : `${distanceFormat.format(activity.distance_meters / 1000)} km`}</div>
          </li>
        ))}
      </ul>
    </Paper>
  );
}

function App() {
  const [report, setReport] = useState<DemoReport>();
  const [selected, setSelected] = useState<string>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>();
  const selectedWeek = report?.weeks.find((week) => week.week_start === selected);

  async function loadDemo() {
    setLoading(true);
    setError(undefined);
    try {
      const response = await fetch('/api/demo/weeks');
      if (!response.ok) throw new Error('Could not load the demo. Check that the backend is running and try again.');
      const data: DemoReport = await response.json();
      setReport(data);
      setSelected(data.weeks[0]?.week_start);
    } catch (failure) {
      setError(failure instanceof Error && !(failure instanceof TypeError) ? failure.message : 'Could not reach the backend.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <Box component="main" className="dashboard">
      <Stack component="header" spacing={1.5} className="hero">
        <Typography variant="body2" color="primary">Endurance Data Platform</Typography>
        <Typography component="h1" className="page-title">Training review</Typography>
        <Typography color="text.secondary">Compare weekly volume and see the sessions behind each total.</Typography>
        <Box><Button variant="contained" onClick={loadDemo} disabled={loading}>{loading ? 'Loading…' : 'Load demo'}</Button></Box>
      </Stack>
      {error && <Alert severity="error">{error}</Alert>}
      {report && <Stack spacing={2}>
        <Stack direction="row" gap={1} flexWrap="wrap">
          <Chip label="Synthetic activities" color="primary" variant="outlined" />
          <Chip label={report.timezone} variant="outlined" />
        </Stack>
        {report.weeks.length === 0 ? <Alert severity="info">No activities to review.</Alert> :
          <WeekChart weeks={report.weeks} selected={selected} onSelect={setSelected} />}
        {selectedWeek && <SessionList week={selectedWeek} timezone={report.timezone} />}
      </Stack>}
    </Box>
  );
}

createRoot(document.getElementById('root')!).render(
  <StrictMode><ThemeProvider theme={theme}><CssBaseline /><App /></ThemeProvider></StrictMode>,
);
