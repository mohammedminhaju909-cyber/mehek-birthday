"""
Mehek's Birthday Surprise 🌸
A single-file Python birthday website (no external packages required).

Run:
    python mehek_birthday.py

Then open:
    http://localhost:8000

To share with Mehek, you can later host the site online.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import random
import json

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Happy Birthday, Mehek 🌸</title>
<style>
  :root {
    --pink: #ffd9e8;
    --pink-deep: #f4a9ca;
    --blue: #d8efff;
    --blue-deep: #8bc9f1;
    --white: #fffdfd;
    --ink: #514654;
    --muted: #897c8b;
    --lilac: #eee3ff;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    min-height: 100vh;
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    color: var(--ink);
    background:
      radial-gradient(circle at 12% 15%, #ffeaf2 0, transparent 27%),
      radial-gradient(circle at 88% 25%, #e5f5ff 0, transparent 29%),
      linear-gradient(145deg, #fffdfd, #fff6fa 52%, #f2faff);
    overflow-x: hidden;
  }
  button, input { font: inherit; }
  button { cursor: pointer; }
  .petal {
    position: fixed; z-index: 0; pointer-events: none;
    opacity: .48; animation: drift 9s ease-in-out infinite;
    font-size: 20px;
  }
  .petal.p1 { left: 7%; top: 18%; }
  .petal.p2 { right: 8%; top: 13%; animation-delay: -3s; }
  .petal.p3 { left: 13%; bottom: 14%; animation-delay: -5s; }
  .petal.p4 { right: 12%; bottom: 16%; animation-delay: -2s; }
  @keyframes drift { 0%,100% { transform: translateY(0) rotate(-8deg); } 50% { transform: translateY(-16px) rotate(9deg); } }
  .wrap {
    position: relative; z-index: 1; width: min(720px, 92%);
    margin: 0 auto; padding: 28px 0 38px;
  }
  .topline {
    display: flex; justify-content: center; align-items: center; gap: 8px;
    color: #9b7f98; font-size: .78rem; letter-spacing: .16em;
    text-transform: uppercase; margin-bottom: 18px;
  }
  .card {
    background: rgba(255,255,255,.83);
    border: 1px solid rgba(255,255,255,.95);
    border-radius: 30px;
    box-shadow: 0 18px 55px rgba(190, 151, 183, .15);
    padding: clamp(24px, 6vw, 48px);
    text-align: center;
    backdrop-filter: blur(12px);
  }
  .flower { font-size: 2.2rem; display: block; margin-bottom: 8px; }
  h1 { font-size: clamp(2.3rem, 8vw, 4.4rem); line-height: 1.03; margin: 10px 0 15px; letter-spacing: -.055em; }
  h1 .name { color: #e78eb6; }
  h2 { font-size: clamp(1.5rem, 5vw, 2rem); margin: 0 0 12px; letter-spacing: -.025em; }
  p { line-height: 1.7; color: var(--muted); }
  .subtitle { max-width: 450px; margin: 0 auto 25px; }
  .pill {
    display: inline-block; padding: 8px 13px; border-radius: 999px;
    background: #f8efff; color: #9b7ab4; font-size: .83rem; margin-bottom: 14px;
  }
  .btn {
    border: 0; border-radius: 999px; padding: 13px 22px; font-weight: 700;
    color: #5b4b60; background: linear-gradient(110deg, var(--pink), var(--blue));
    box-shadow: 0 7px 17px rgba(206, 158, 194, .18);
    transition: transform .18s ease, box-shadow .18s ease;
  }
  .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 22px rgba(206, 158, 194, .25); }
  .btn.secondary { background: #fff; border: 1px solid #f1dce9; box-shadow: none; }
  .actions { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-top: 20px; }
  .screen { display: none; }
  .screen.active { display: block; animation: appear .45s ease both; }
  @keyframes appear { from { opacity: 0; transform: translateY(9px); } to { opacity: 1; transform: translateY(0); } }
  .gamebox {
    margin: 22px auto 12px; max-width: 390px; padding: 20px;
    border-radius: 22px; background: linear-gradient(135deg, #fff3f8, #eff8ff);
    border: 1px solid #fff;
  }
  .guess-row { display: flex; gap: 9px; max-width: 290px; margin: 16px auto 0; }
  input[type=number] {
    min-width: 0; width: 100%; border: 1px solid #edd9e8; background: white;
    padding: 12px 14px; border-radius: 14px; outline: none; color: var(--ink);
  }
  input:focus { border-color: #dba9d2; box-shadow: 0 0 0 3px #f8e8f4; }
  .feedback { min-height: 28px; font-weight: 700; color: #b478a0; margin: 12px 0 0; }
  .chocolate { font-size: 4.5rem; margin: 6px 0; display: inline-block; animation: bob 2.2s ease-in-out infinite; }
  @keyframes bob { 0%,100% { transform: rotate(-4deg) translateY(0); } 50% { transform: rotate(4deg) translateY(-7px); } }
  .gift {
    margin: 20px auto; max-width: 390px; border-radius: 22px; padding: 23px;
    background: linear-gradient(140deg, #fff0f6, #edf8ff);
    border: 1px dashed #e8bfd8;
  }
  .hidden-message { display: none; }
  .hidden-message.show { display: block; animation: appear .55s ease both; }
  .signature { margin-top: 30px; font-size: .9rem; color: #a18ca2; }
  .signature strong { display: block; margin-top: 6px; color: #d184ac; font-weight: 700; }
  .confetti {
    position: fixed; z-index: 10; top: -20px; width: 9px; height: 13px;
    border-radius: 3px; pointer-events: none; animation: fall 2.8s linear forwards;
  }
  @keyframes fall { to { transform: translateY(110vh) rotate(720deg); opacity: .1; } }
  .tiny { font-size: .84rem; }
  footer { text-align: center; color: #b5a2b4; font-size: .8rem; padding: 20px 8px 0; }
  @media (max-width: 480px) {
    .wrap { padding-top: 18px; }
    .card { border-radius: 24px; }
    .guess-row { flex-direction: column; }
  }
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; }
  }
</style>
</head>
<body>
<div class="petal p1">🌸</div><div class="petal p2">✿</div>
<div class="petal p3">🌷</div><div class="petal p4">🌸</div>

<main class="wrap">
  <div class="topline">a tiny website made with care <span>✧</span> just for you</div>
  <section class="card">
    <div id="welcome" class="screen active">
      <span class="flower">🌸</span>
      <div class="pill">a little birthday universe</div>
      <h1>Happy Birthday,<br><span class="name">Mehek!</span></h1>
      <p class="subtitle">Today is your day, so I made you a tiny adventure. There may be a few surprises hiding inside… 👀</p>
      <div style="font-size:2rem; margin: 12px 0 22px;">🎈　🧁　🎈</div>
      <button class="btn" onclick="goTo('game')">Open your surprise ✨</button>
    </div>

    <div id="game" class="screen">
      <span class="flower">🎮</span>
      <div class="pill">level 1 · the guessing game</div>
      <h2>Guess the secret number</h2>
      <p>I'm thinking of a number from <strong>1 to 20</strong>.<br>Can you find it, birthday girl?</p>
      <div class="gamebox">
        <div style="font-size:2rem;">🔢</div>
        <div class="guess-row">
          <input id="guess" type="number" min="1" max="20" placeholder="Your guess…" aria-label="Guess a number">
          <button class="btn" onclick="checkGuess()">Guess!</button>
        </div>
        <div id="feedback" class="feedback" aria-live="polite">You have 5 tries. Good luck! 🌷</div>
        <p class="tiny" id="tries">Tries left: 5</p>
      </div>
      <p class="tiny">Psst… winning unlocks the next little surprise.</p>
      <div class="actions"><button class="btn secondary" onclick="goTo('welcome')">Back</button></div>
    </div>

    <div id="choco" class="screen">
      <span class="flower">🍫</span>
      <div class="pill">level 2 · chocolate unlocked</div>
      <h2>Okay, chocolate lover…</h2>
      <div class="chocolate">🍫</div>
      <p class="subtitle">A tiny virtual milk-chocolate delivery, because your birthday deserves something sweet.</p>
      <div class="gift">
        <p style="margin-top:0;">🥛 <strong>Milk chocolate mood:</strong> activated</p>
        <p class="tiny">Warning: this button contains an unreasonable amount of cuteness.</p>
        <button class="btn" onclick="revealGift()">Open the suspiciously cute gift 🎁</button>
      </div>
      <div id="giftMessage" class="hidden-message">
        <h2>WAIT—THERE'S MORE?! 😭💗</h2>
        <p>Surprise, Mehek! 🌸</p>
        <p>You deserve a day full of laughter, sweet moments, unexpected happiness, and all the little things that make you smile.</p>
        <p>May this new year of your life be as lovely as your favourite things. Keep being wonderfully you. 🩵</p>
        <div style="font-size:2.4rem;">🎉 🎂 🦋 🌸 🎉</div>
        <div class="signature">
          <span>with a little chaos and a lot of thought,</span>
          <strong>made by an illogical thinker, met by chance ✧</strong>
        </div>
      </div>
      <div class="actions"><button class="btn secondary" onclick="goTo('game')">Play again</button></div>
    </div>
  </section>
  <footer>made of pastel skies, tiny flowers & a birthday wish 🌸</footer>
</main>

<script>
  let secret = Math.floor(Math.random() * 20) + 1;
  let triesLeft = 5;
  let won = false;

  function goTo(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    if (id === 'game') setTimeout(() => document.getElementById('guess').focus(), 100);
    window.scrollTo({top: 0, behavior: 'smooth'});
  }

  function checkGuess() {
    if (won) { goTo('choco'); return; }
    const input = document.getElementById('guess');
    const value = Number(input.value);
    const feedback = document.getElementById('feedback');
    if (!input.value || !Number.isInteger(value) || value < 1 || value > 20) {
      feedback.textContent = 'Pick a whole number from 1 to 20, bestie! 🌸';
      return;
    }
    triesLeft--;
    if (value === secret) {
      won = true;
      feedback.textContent = 'YOU GOT IT!! Birthday genius detected. 🎉';
      document.getElementById('tries').textContent = 'Game cleared!';
      confetti();
      setTimeout(() => goTo('choco'), 1250);
      return;
    }
    if (triesLeft <= 0) {
      feedback.textContent = `The secret number was ${secret}! No worries—surprises wait for you anyway. 💗`;
      document.getElementById('tries').textContent = 'Out of tries — surprise unlocked!';
      won = true;
      setTimeout(() => goTo('choco'), 1800);
      return;
    }
    feedback.textContent = value < secret ? 'A little higher! ⬆️' : 'A little lower! ⬇️';
    document.getElementById('tries').textContent = `Tries left: ${triesLeft}`;
    input.value = '';
    input.focus();
  }

  document.getElementById('guess').addEventListener('keydown', event => {
    if (event.key === 'Enter') checkGuess();
  });

  function revealGift() {
    document.getElementById('giftMessage').classList.add('show');
    confetti();
    document.getElementById('giftMessage').scrollIntoView({behavior: 'smooth', block: 'center'});
  }

  function confetti() {
    const symbols = ['🌸', '✿', '💗', '🩵', '✨', '🎉'];
    const colors = ['#f6a8ca', '#9bd8f6', '#d9c5ff', '#ffe4a8', '#b9e8d1'];
    for (let i = 0; i < 42; i++) {
      const bit = document.createElement('div');
      bit.className = 'confetti';
      bit.textContent = Math.random() > .55 ? symbols[Math.floor(Math.random() * symbols.length)] : '';
      bit.style.left = Math.random() * 100 + 'vw';
      bit.style.background = colors[Math.floor(Math.random() * colors.length)];
      bit.style.animationDelay = Math.random() * .7 + 's';
      bit.style.animationDuration = (2 + Math.random() * 1.7) + 's';
      bit.style.transform = `rotate(${Math.random() * 360}deg)`;
      document.body.appendChild(bit);
      setTimeout(() => bit.remove(), 4500);
    }
  }
</script>
</body>
</html>
"""

class BirthdayHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404, "Not found")
            return
        content = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), BirthdayHandler)
    print("\\n🌸 Mehek's birthday website is running!")
    print("Open http://localhost:8000 in your browser.")
    print("Press Ctrl+C to stop the server.\\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nBirthday server stopped. Bye!")
        server.server_close()
