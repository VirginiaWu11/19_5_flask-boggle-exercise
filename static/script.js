words = [];
score = 0;
secs = 60;
function showMessage(msg, cls) {
  // show message on html
  $(".msg").text(msg).removeClass().addClass(`msg ${cls}`);
}

function updateScore() {
  $(".score").text(score);
}

$("#add-word").on("submit", handleSubmit);

async function handleSubmit(evt) {
  evt.preventDefault();
  let guess = $("#guess").val();
  if (!guess) return;

  if (words.includes(guess)) {
    showMessage(`Already found ${guess}`, "error");
  }
  //   check server for validity
  const resp = await axios.get("/check-guess", { params: { guess: guess } });
  if (resp.data.result === "not-word") {
    showMessage(`${guess.toUpperCase()} is not in our dictionary`, "error");
  } else if (resp.data.result === "not-on-board") {
    showMessage(
      `${guess.toUpperCase()} is not a valid word on this board`,
      "error"
    );
  } else {
    showMessage(`${guess.toUpperCase()} scored ${guess.length} points!`, "ok");
    score += guess.length;
    updateScore();
  }
  $("#guess").val("");
}

function showTimer() {
  $(".timer").text(secs);
}

function timer() {
  let time = setInterval(function () {
    secs -= 1;
    showTimer();
    if (secs === 0) {
      clearInterval(time);
      $("#add-word").hide();
      scoreGame();
    }
  }, 1000);
}
timer();

async function scoreGame() {
  const resp = await axios.post("/post-score", { score: score });
  if (resp.data.brokeRecord) {
    showMessage(`Congratulations! New record: ${score}`, "ok");
  } else {
    showMessage(`Game Over. Final Score: ${score}`, "ok");
  }
}
