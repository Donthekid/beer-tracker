let currentTab = 'total';

function switchTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
  document.querySelector(`.tab-button[onclick*="${tab}"]`).classList.add('active');
  updateLeaderboard();
}

async function addBeer(user, amount) {
  const res = await fetch('/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: user, count: amount })
  });

  if (res.ok) {
    const data = await res.json();
    const userCard = document.querySelector(`[data-user="${user}"]`);
    const countEl = userCard.querySelector('.beer-count');
    countEl.textContent = data.new_total;

    if (amount === 5) showWoman();

    updateLeaderboard();
    updateTotalBeers();
  }
}

function updateLeaderboard() {
  const leaderboard = [];

  document.querySelectorAll('.user-card').forEach(card => {
    const name = card.getAttribute('data-user');
    const beers = parseInt(card.querySelector('.beer-count').textContent);
    leaderboard.push({ name, beers });
  });

  leaderboard.sort((a, b) => {
    if (b.beers !== a.beers) return b.beers - a.beers;
    return a.name.localeCompare(b.name);
  });

  const container = document.getElementById('leaderboard-container');
  container.innerHTML = '';

  const maxBeers = leaderboard[0]?.beers || 1;

  leaderboard.forEach((user, i) => {
    const row = document.createElement('div');
    row.className = 'leaderboard-row';

    const xpBarWidth = Math.round((user.beers / maxBeers) * 100);
    const title = getTitle(i, user.beers);

    row.innerHTML = `
      <div class="left">
        <div class="name">${user.name}</div>
        <span class="title-tag">${title}</span>
        <div class="count">${user.beers} 🍺</div>
        <div class="bar-wrapper"><div class="bar" style="width: ${xpBarWidth}%"></div></div>
      </div>
      <div class="buttons">
        <button onclick="addBeer('${user.name}', 1)">+1</button>
        <button onclick="addBeer('${user.name}', 5)">+5</button>
      </div>
    `;

    container.appendChild(row);
  });
}

function getTitle(rank, beers) {
  if (beers === 0) return "Virgin";
  if (rank === 0) return "Alcoholic in Chief";
  if (rank === 1) return "Deputy Degenerate";
  if (rank === 2) return "Brewskeeter";
  if (rank === 3) return "Pilsner Prodigy";
  if (rank === 4) return "Certified Sipper";
  return "";
}

function updateTotalBeers() {
  let total = 0;
  document.querySelectorAll('.beer-count').forEach(el => {
    total += parseInt(el.textContent);
  });
  document.getElementById('total-beers').textContent = total;
}

function showWoman() {
  const woman = document.getElementById('woman-container');
  woman.innerText = '💃🍺🍺🍺🍺🍺';
  woman.classList.add('show');
  const audio = new Audio('https://www.myinstants.com/media/sounds/alcoholic.mp3');
  audio.play();
  setTimeout(() => {
    woman.classList.remove('show');
  }, 1500);
}

window.onload = () => {
  updateLeaderboard();
  updateTotalBeers();
};

