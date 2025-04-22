let currentTab = 'total';

// 🍺 Log beers
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

    await addToToastFeed(user, amount);

    if (amount === 5) showWoman();
    updateLeaderboard();
    updateTotalBeers();
  }
}

// 🔁 Add toast to global server-side log
async function addToToastFeed(name, count) {
  await fetch('/toast', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, count })
  });
}

// 🔁 Load shared toast feed from server
async function loadToasts() {
  const res = await fetch('/toast');
  const feed = await res.json();

  const list = document.getElementById('toast-list');
  if (!list) return;

  list.innerHTML = '';
  feed.slice().reverse().forEach(toast => {
    const time = new Date(toast.timestamp);
    const li = document.createElement('li');
    li.innerHTML = `${toast.name} has logged <strong>${toast.count}</strong> beers<br><span class="toast-time">${time.toLocaleDateString()} @ ${time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>`;
    list.appendChild(li);
  });
}

// 📊 Update leaderboard
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

    const title = getTitle(i, user.beers);
    const xp = Math.round((user.beers / maxBeers) * 100);

    row.innerHTML = `
      <div class="left">
        <div class="name">${user.name}</div>
        <span class="title-tag">${title}</span>
        <div class="count">${user.beers} 🍺</div>
        <div class="bar-wrapper"><div class="bar" style="width: ${xp}%"></div></div>
      </div>
      <div class="buttons">
        <button onclick="addBeer('${user.name}', 1)">+1</button>
        <button onclick="addBeer('${user.name}', 5)">+5</button>
      </div>
    `;

    container.appendChild(row);
  });
}

// 🏅 Rank title logic
function getTitle(rank, beers) {
  if (beers === 0) return "Virgin";
  if (rank === 0) return "Alcoholic in Chief";
  if (rank === 1) return "Deputy Degenerate";
  if (rank === 2) return "Brewskeeter";
  if (rank === 3) return "Pilsner Prodigy";
  if (rank === 4) return "Certified Sipper";
  return "Weekend Warrior";
}

// 📈 Update total beers and progress bar

function updateTotalBeers() {
  let total = 0;
  document.querySelectorAll('.beer-count').forEach(el => {
    total += parseInt(el.textContent);
  });
  document.getElementById('total-beers').textContent = total;

  const percent = Math.min((total / 1000000) * 100, 100).toFixed(2);
  document.getElementById('million-bar').style.width = `${percent}%`;
  document.getElementById('million-count').textContent = `${total} beers (${percent}%)`;
}

// 💃 Woman animation
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

// 🔐 Toggle Admin Panel
window.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.key === '`') {
    const panel = document.getElementById('admin-panel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
  }
});

// 🔐 Admin: Adjust beers
async function submitBeerAdjustment() {
  const name = document.getElementById('admin-name').value.trim();
  const amount = parseInt(document.getElementById('admin-amount').value);

  if (!name || isNaN(amount)) {
    alert("Please enter both a name and number.");
    return;
  }

  const res = await fetch('/admin/adjust', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: name, count: amount })
  });

  if (res.ok) {
    alert(`Adjusted ${name} by ${amount} beers!`);
    location.reload();
  } else {
    alert("Failed to apply change.");
  }
}

// 👑 Admin: Set AOTW
async function submitAOTW() {
  const name = document.getElementById('aotw-name-input').value.trim();
  const image = document.getElementById('aotw-image-input').value.trim();
  const message = document.getElementById('aotw-message-input').value.trim();

  if (!name || !image || !message) {
    alert("Please fill in all AOTW fields.");
    return;
  }

  const res = await fetch('/admin/set_aotw', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, image, message })
  });

  if (res.ok) {
    alert("AOTW updated!");
    location.reload();
  } else {
    alert("Failed to update AOTW.");
  }
}

// 🏁 On page load
window.onload = () => {
  updateLeaderboard();
  updateTotalBeers();
  loadToasts();
  setInterval(loadToasts, 10000);
};

let adminMode = false;

document.addEventListener("keydown", (e) => {
  if (e.key === ",") {
    adminMode = !adminMode;
    document.getElementById("admin-panel").style.display = adminMode ? "block" : "none";
  }
});

async function adminAdjust() {
  const user = document.getElementById("admin-name").value;
  const amount = document.getElementById("admin-amount").value;

  const res = await fetch(`/admin-adjust?user=${user}&amount=${amount}`);
  const msg = await res.text();
  alert(msg);
  updateLeaderboard();
  updateTotalBeers();
}

async function setAOTW() {
  const name = document.getElementById("aotw-name").value;
  const caption = document.getElementById("aotw-caption").value;
  const image = document.getElementById("aotw-image").value;

  const res = await fetch(`/set-aotw?name=${encodeURIComponent(name)}&caption=${encodeURIComponent(caption)}&image=${encodeURIComponent(image)}`);
  const msg = await res.text();
  alert(msg);
  location.reload();
}

