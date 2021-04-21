words = [];
score = 0;

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
  console.log(guess);
  if (!guess) return;

  if (words.includes(guess)) {
    showMessage(`Already found ${guess}`, "error");
  }
  //   check server for validity
  const resp = await axios.get("/check-guess", { params: { guess: guess } });
  console.log(resp.data.result);
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
