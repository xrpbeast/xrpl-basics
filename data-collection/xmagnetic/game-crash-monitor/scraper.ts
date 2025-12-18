/**
 * xMagnetic Crash Game Historical Data Scraper
 * Downloads ALL game data from game #1 to latest
 */

import * as fs from "fs";

const DATA_DIR = "./data";
const FULL_GAMES_FILE = `${DATA_DIR}/full_games.jsonl`;
const PROGRESS_FILE = `${DATA_DIR}/scrape_progress.json`;

// Rate limiting - be nice to their server
const DELAY_MS = 5 // 50ms between requests = 20 req/sec
const BATCH_SIZE = 1000; // Save progress every 100 games
const CONCURRENT_REQUESTS = 10; // Parallel requests

interface GameData {
  gameNumber: number;
  timeStart: string;
  timeEnd: string;
  currentCoef: number;
  totalBets: number;
  totalFees: number;
  totalWins: number;
  magBurned: number;
  gameEnded: boolean;
  bets: BetData[];
  lefter: string[]; // wallets that cashed out
}

interface BetData {
  wallet: string;
  amount: number;
  betResult: {
    coef: number;
    wonAmount: number;
  };
}

interface Progress {
  lastGameId: number;
  totalGames: number;
  startedAt: string;
  lastUpdated: string;
}

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

const log = (msg: string) => {
  const ts = new Date().toISOString().slice(11, 19);
  console.log(`[${ts}] ${msg}`);
};

const loadProgress = (): Progress | null => {
  if (fs.existsSync(PROGRESS_FILE)) {
    return JSON.parse(fs.readFileSync(PROGRESS_FILE, "utf-8"));
  }
  return null;
};

const saveProgress = (progress: Progress) => {
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(progress, null, 2));
};

const fetchGame = async (gameId: number): Promise<GameData | null> => {
  try {
    const res = await fetch(
      `https://crashapi.xmagnetic.org/GetGameById?gameId=${gameId}`,
      {
        headers: {
          "User-Agent": "Mozilla/5.0 (compatible; research)",
        },
      }
    );
    if (!res.ok) return null;
    return await res.json();
  } catch (e) {
    return null;
  }
};

const fetchLatestGameId = async (): Promise<number> => {
  const res = await fetch(
    "https://crashapi.xmagnetic.org/GetCrashSettings?countGames=1"
  );
  const data = await res.json();
  return data.last100Games?.[0]?.gameNumber || 0;
};

const scrape = async () => {
  console.log("\n" + "=".repeat(60));
  console.log("🕷️  xMagnetic Crash Game Scraper");
  console.log("=".repeat(60) + "\n");

  // Get latest game ID
  const latestGameId = await fetchLatestGameId();
  log(`Latest game: #${latestGameId}`);

  // Check for existing progress
  let progress = loadProgress();
  let startId = 1;

  if (progress) {
    startId = progress.lastGameId + 1;
    log(`Resuming from game #${startId} (${progress.lastGameId} already scraped)`);
  } else {
    progress = {
      lastGameId: 0,
      totalGames: latestGameId,
      startedAt: new Date().toISOString(),
      lastUpdated: new Date().toISOString(),
    };
    // Clear existing file if starting fresh
    if (fs.existsSync(FULL_GAMES_FILE)) {
      fs.unlinkSync(FULL_GAMES_FILE);
    }
  }

  const totalToFetch = latestGameId - startId + 1;
  log(`Games to fetch: ${totalToFetch}`);

  // Estimate time
  const estimatedSeconds = (totalToFetch * DELAY_MS) / 1000 / CONCURRENT_REQUESTS;
  const estimatedMinutes = Math.ceil(estimatedSeconds / 60);
  log(`Estimated time: ~${estimatedMinutes} minutes\n`);

  let fetched = 0;
  let errors = 0;
  let gamesWithBets = 0;
  let totalBetAmount = 0;
  const startTime = Date.now();

  // Process in batches
  for (let batchStart = startId; batchStart <= latestGameId; batchStart += BATCH_SIZE) {
    const batchEnd = Math.min(batchStart + BATCH_SIZE - 1, latestGameId);
    const batchGames: GameData[] = [];

    // Fetch batch with concurrency
    const ids = Array.from({ length: batchEnd - batchStart + 1 }, (_, i) => batchStart + i);
    
    for (let i = 0; i < ids.length; i += CONCURRENT_REQUESTS) {
      const chunk = ids.slice(i, i + CONCURRENT_REQUESTS);
      const results = await Promise.all(chunk.map(fetchGame));
      
      for (const game of results) {
        if (game) {
          batchGames.push(game);
          fetched++;
          if (game.bets && game.bets.length > 0) {
            gamesWithBets++;
            totalBetAmount += game.bets.reduce((sum, b) => sum + b.amount, 0);
          }
        } else {
          errors++;
        }
      }
      
      await sleep(DELAY_MS);
    }

    // Append batch to file
    for (const game of batchGames) {
      fs.appendFileSync(FULL_GAMES_FILE, JSON.stringify(game) + "\n");
    }

    // Update progress
    progress.lastGameId = batchEnd;
    progress.lastUpdated = new Date().toISOString();
    saveProgress(progress);

    // Progress report
    const pct = (((batchEnd - startId + 1) / totalToFetch) * 100).toFixed(1);
    const elapsed = (Date.now() - startTime) / 1000;
    const rate = fetched / elapsed;
    const eta = Math.ceil((latestGameId - batchEnd) / rate / 60);
    
    log(
      `Progress: ${pct}% | Games: ${fetched} | With bets: ${gamesWithBets} | ` +
      `Errors: ${errors} | ETA: ${eta}min`
    );
  }

  console.log("\n" + "=".repeat(60));
  console.log("✅ SCRAPING COMPLETE");
  console.log("=".repeat(60));
  console.log(`   Total games: ${fetched}`);
  console.log(`   Games with bets: ${gamesWithBets}`);
  console.log(`   Total XRP bet: ${totalBetAmount.toFixed(2)}`);
  console.log(`   Errors: ${errors}`);
  console.log(`   Data file: ${FULL_GAMES_FILE}`);
  console.log("=".repeat(60) + "\n");
};

scrape().catch(console.error);
