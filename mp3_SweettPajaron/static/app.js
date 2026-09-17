// Points to your local backend proxy server route
function getProxyStreamUrl(id) {
  return `/stream/${id}`;
}

const songData = [
  {
    id: 1,
    title: "Rewrite The Stars",
    artist: "Anne-Marie, James Arthur",
    album: "The Greatest Showman",
    albumArt: getProxyStreamUrl("1ZkZm5-KWP56g09MeQs_kG3dZmUW_e-gB"),
    audioUrl: getProxyStreamUrl("1lK8zdzqtYSig4T86x1n8JRtElH1mRBA0"),
    lyrics: `You know I want you
It's not a secret I try to hide
I know you want me
So don't keep saying our hands are tied

You think it's easy
You think I'm holding on to you
When there are mountains
And there are doors that we can't pass through`
  },
  {
    id: 2,
    title: "Bocil",
    artist: "Bocil",
    album: "Single",
    albumArt: getProxyStreamUrl(),
    audioUrl: getProxyStreamUrl("1qfDCqndNu4YYOttzhJ9x-ztJLDj57qB3"),
    lyrics: `[Lyrics for Bocil]`
  },
  {
    id: 3,
    title: "Consume",
    artist: "Chase Atlantic",
    album: "BEAUTY IN DEATH",
    albumArt: getProxyStreamUrl(),
    audioUrl: getProxyStreamUrl("1advcGdG4AJyKNJuCWJpwa_EqzXDh3lQi"),
    lyrics: `She said, "Careful or you'll lose it"
She said, "Careful or you'll lose it"
'Cause my hearts cold, but it's beatin'
She said, "Careful or you'll lose it"`
  },
  {
    id: 4,
    title: "I Wanna Be Yours",
    artist: "Arctic Monkeys",
    album: "AM",
    albumArt: getProxyStreamUrl(),
    audioUrl: getProxyStreamUrl("1c0eJKYNzOUdBHlIi2MU52OKxE85nLAzy"),
    lyrics: `I wanna be your vacuum cleaner
Breathing in your dust
I wanna be your Ford Cortina
I will never rust`
  },
  {
    id: 5,
    title: "Let Down",
    artist: "Radiohead",
    album: "OK Computer",
    albumArt: getProxyStreamUrl(),
    audioUrl: getProxyStreamUrl("10nkGimGMFJ2CtXNuuHW2anWftR-gAZfN"),
    lyrics: `Transport, motorways and tramlines
Starting and then stopping
Taking off and landing
The emptiest of feelings`
  }
];

let currentSongIndex = 0;
let isPlaying = false;

document.addEventListener("DOMContentLoaded", () => {
  const audioPlayer = document.getElementById("audioPlayer");
  const songList = document.getElementById("songList");
  const playPauseBtn = document.getElementById("playerPlayPauseBtn");
  const playFromDetailBtn = document.getElementById("playFromDetailBtn");
  
  const backToHomeBtn = document.getElementById("backToHomeBtn");
  const backToHomeFromDetailBtn = document.getElementById("backToHomeFromDetailBtn");

  renderSongList();

  function renderSongList() {
    if (!songList) return;
    songList.innerHTML = "";
    songData.forEach((song, index) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <img src="${song.albumArt}" alt="${song.title}" class="song-art-list">
        <div class="song-info-list">
          <h3>${song.title}</h3>
          <p>${song.artist} - ${song.album}</p>
        </div>
      `;
      li.addEventListener("click", () => openSongDetail(index));
      songList.appendChild(li);
    });
  }

  function openSongDetail(index) {
    currentSongIndex = index;
    const song = songData[index];
    document.getElementById("detailAlbumArt").src = song.albumArt;
    document.getElementById("detailTrackTitle").textContent = song.title;
    document.getElementById("detailTrackArtist").textContent = song.artist;
    document.getElementById("detailAlbumName").textContent = song.album;
    showPage("songDetailPage", "detail-active-bg");
  }

  function loadAndPlaySong(index) {
    currentSongIndex = index;
    const song = songData[index];
    
    audioPlayer.src = song.audioUrl;
    document.getElementById("playerTrackTitle").textContent = song.title;
    document.getElementById("playerTrackArtist").textContent = song.artist;
    document.getElementById("albumArt").src = song.albumArt;

    const formattedLyrics = song.lyrics.replace(/\n/g, '<br>');
    document.getElementById("lyricsContainer").innerHTML = `<p>${formattedLyrics}</p>`;

    audioPlayer.play().then(() => {
      isPlaying = true;
      updatePlayBtn();
    }).catch(err => {
      console.error("Playback error:", err);
      alert("Playback failed. Please restart server.py and refresh the page.");
    });

    showPage("playerPage", "player-active-bg");
  }

  function updatePlayBtn() {
    playPauseBtn.innerHTML = isPlaying ? `<i class="fas fa-pause"></i>` : `<i class="fas fa-play"></i>`;
  }

  function showPage(pageId, bgClass) {
    document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
    document.body.className = bgClass || "";
    document.getElementById(pageId).classList.add("active");
  }

  playPauseBtn.addEventListener("click", () => {
    if (isPlaying) {
      audioPlayer.pause();
      isPlaying = false;
    } else {
      audioPlayer.play().then(() => {
        isPlaying = true;
      }).catch(err => console.error("Playback error:", err));
    }
    updatePlayBtn();
  });

  playFromDetailBtn.addEventListener("click", () => loadAndPlaySong(currentSongIndex));
  backToHomeBtn.addEventListener("click", () => showPage("homePage"));
  backToHomeFromDetailBtn.addEventListener("click", () => showPage("homePage"));

  audioPlayer.addEventListener("timeupdate", () => {
    const progressBar = document.getElementById("playerProgressBar");
    const currentTimeEl = document.getElementById("playerCurrentTime");
    const totalDurationEl = document.getElementById("playerTotalDuration");

    if (audioPlayer.duration) {
      const pct = (audioPlayer.currentTime / audioPlayer.duration) * 100;
      progressBar.style.width = `${pct}%`;

      let curMins = Math.floor(audioPlayer.currentTime / 60);
      let curSecs = Math.floor(audioPlayer.currentTime % 60);
      let durMins = Math.floor(audioPlayer.duration / 60);
      let durSecs = Math.floor(audioPlayer.duration % 60);

      if (curSecs < 10) curSecs = `0${curSecs}`;
      if (durSecs < 10) durSecs = `0${durSecs}`;

      currentTimeEl.textContent = `${curMins}:${curSecs}`;
      totalDurationEl.textContent = `${durMins}:${durSecs}`;
    }
  });
});