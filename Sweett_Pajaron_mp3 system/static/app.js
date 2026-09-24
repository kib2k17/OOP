document.addEventListener("DOMContentLoaded", () => {
  
  const songs = [
    // ROCK
    {
      id: 1,
      title: "Dream On",
      artist: "Aerosmith",
      album: "Aerosmith",
      genre: "Rock",
      cover: "https://drive.google.com/file/d/1leaBYQ5HMpdrY28grQHuBY2c_dQE1uaE/view?usp=drive_link",
      src: "https://drive.google.com/file/d/1gnQmsiB46TmocuJEjvx6pgJFbBH10pvD/view?usp=drive_link"
    },
    {
      id: 2,
      title: "Smoke On The Water",
      artist: "Deep Purple",
      album: "Machine Head",
      genre: "Rock",
      cover: "https://drive.google.com/file/d/1Ju_LObVGLyA6JBGkK73boMXiF6tyKkb9/view?usp=drive_link",
      src: "https://drive.google.com/file/d/1fgv0hWLa33Ou26-4Ceq8WY2BB77zorr7/view?usp=drive_link"
    },
    {
      id: 3,
      title: "Don't Stop Believin'",
      artist: "Journey",
      album: "Escape",
      genre: "Rock",
      cover: "https://drive.google.com/file/d/1_Yiij4esSEMRQH1XmY1eGO72WJVaPEe1/view?usp=drive_link",
      src: "https://drive.google.com/file/d/174Am2Cl4QwJ3vqvt19Bt-ViCbGH1m24e/view?usp=drive_link"
    },
    {
      id: 4,
      title: "Bohemian Rhapsody",
      artist: "Queen",
      album: "A Night at the Opera",
      genre: "Rock",
      cover: "https://drive.google.com/file/d/1EslkXr2Khvvim17QdSajuvMUVm5Z2Gq3/view?usp=drive_link",
      src: "https://drive.google.com/file/d/174Am2Cl4QwJ3vqvt19Bt-ViCbGH1m24e/view?usp=drive_link"
    },
    {
      id: 5,
      title: "Baba O'Riley",
      artist: "The Who",
      album: "Who's Next",
      genre: "Rock",
      cover: "https://drive.google.com/file/d/149NH8q_zh_oXBo2MuvWvPjwIva3wf6Vf/view?usp=drive_link",
      src: "https://drive.google.com/file/d/1YIO8EmD-OKBCQJ4MpshAMhVFBItLApj8/view?usp=drive_link"
    },

    // LOVE SONGS
    {
      id: 6,
      title: "Kathang Isip",
      artist: "ben&Ben",
      album: "÷ Limasawa Street",
      genre: "Love Songs",
      cover: "https://drive.google.com/file/d/1AUyHEWPRDgYuMheB4lt62XEu2NPvH-Dj/view?usp=drive_link",
      src: "https://drive.google.com/file/d/1b241QjYpOVT8fwIYkZFg8Nyh7fwba1Qc/view?usp=drive_link"
    },
    {
      id: 7,
      title: "Your Song",
      artist: "Parokya Ni Edgar",
      album: "bitgotilyo",
      genre: "Love Songs",
      cover: "https://drive.google.com/file/d/1ymQ7dhBypI7LZmGe0AVuFjFqs3nKC5yq/view?usp=drive_link",
      src: "https://drive.google.com/file/d/1x-FahwhZik9Dw0BIYsLZDfLNOv6h5BlM/view?usp=drive_link"
    },
    {
      id: 8,
      title: "Passenger Seat",
      artist: "Stephen Speaks",
      album: "Doubdting Thomas",
      genre: "Love Songs",
      cover: "https://drive.google.com/file/d/1hmixfCCLYvADSRawNwt_0aGR7quWme9L/view?usp=drive_link",
      src: "https://drive.google.com/file/d/1Rt4Oi-LUdUGVsvKkt3UfyfiGAB412Mvg/view?usp=drive_link"
    },
    {
      id: 9,
      title: "214",
      artist: "Rivermaya",
      album: "Rivermaya",
      genre: "Love Songs",
      cover: "https://drive.google.com/file/d/1H8Cx7QHchB4ixq8kyPJawRIAobdqIYOU/view?usp=drive_link",
      src: "https://drive.google.com/file/d/1kRPKCB-tyyK1HXYdjPA6p5dhCd2l7J3I/view?usp=drive_link"
    },
    {
      id: 10,
      title: "up dharma down",
      artist: "UDD",
      album: "Bipolar",
      genre: "Love Songs",
      cover: "https://drive.google.com/file/d/1L430itTB2oXuq_VKAzjotXzZqcuI4SuZ/view?usp=drive_link",
      src: "https://drive.google.com/file/d/1-iTUO-lOKxpNN4DszD1NqjYx2j22l-62/view?usp=drive_link"
    },

    // COUNTRY
    {
      id: 11,
      title: "CRAZY",
      artist: "Patsy Cline",
      album: "Showecase",
      genre: "Country",
      cover: "https://drive.google.com/file/d/154sdj-WOMVogdylP5LmDYCCO6XGgmD7s/view?usp=drive_link",
      src: "https://drive.google.com/file/d/12QG2BXpUpP1SXtn_Y0aexGblMe0PqNGS/view?usp=sharing"
    },
    {
      id: 12,
      title: "He Stopped Loving Her Today",
      artist: "George Jones",
      album: "I Am What I Am",
      genre: "Country",
      cover: "https://drive.google.com/file/d/1reDQEm8MpYtrtcC-zck4AwwLfGjPFc4B/view?usp=drive_link",
      src: "https://drive.google.com/file/d/17Ugh0oESJHan-5Q4SXVb-4U2Gl0wzfD6/view?usp=drive_link"
    },
    {
      id: 13,
      title: "Jolene",
      artist: "Dolly Parton",
      album: "Jolene",
      genre: "Country",
      cover: "https://drive.google.com/file/d/1aVzVUU-b6b0fIZl9Rqlm68ae9Iz0xz2M/view?usp=drive_link",
      src: "https://drive.google.com/file/d/12i0Jf3pLa6_hMkc40VYRmu5KHNBpJIUi/view?usp=drive_link"
    },
    {
      id: 14,
      title: "Ring of Fire",
      artist: "Johnny Cash",
      album: "Ring of Fire: The Best of Johnny Cash",
      genre: "Country",
      cover: "https://drive.google.com/file/d/1VIBNtOa3l3yKKBizn8zMX5sBTIlH0n6i/view?usp=drive_link",
      src: "https://drive.google.com/file/d/1FXJblxQatlarknGaWysRXAudeIlRhJZV/view?usp=drive_link"
    },
    {
      id: 15,
      title: "King of the Road ",
      artist: "Roger Miller",
      album: "The Return of Roger Miller",
      genre: "Country",
      cover: "https://drive.google.com/file/d/1WFkUq9wrd5UHJzeeR_XsYc6okWF-LpC7/view?usp=drive_link",
      src: "https://drive.google.com/file/d/1amFaJL-KBnbB9lyzWXsMnSVWeIRs6kvf/view?usp=drive_link"
    }
  ];

  // Helper function to handle Google Drive URLs & proxy streams
  function fixDriveUrl(url, isAudio = false) {
    if (!url) return "";
    if (url.includes("drive.google.com")) {
      const match = url.match(/\/d\/([a-zA-Z0-9_-]+)/) || url.match(/id=([a-zA-Z0-9_-]+)/);
      if (match && match[1]) {
        const fileId = match[1];
        return isAudio 
          ? `/stream?id=${fileId}`
          : `https://lh3.googleusercontent.com/d/${fileId}`;
      }
    }
    return url;
  }

  // Pre-process song links
  const processedSongs = songs.map((song) => ({
    ...song,
    cover: fixDriveUrl(song.cover, false),
    src: fixDriveUrl(song.src || song.url || song.audio, true)
  }));

  let currentFilter = "All";
  let currentSong = null;

  const songListEl = document.getElementById("songList");
  const genreTabsEl = document.getElementById("genreTabs");
  const noSongsMsg = document.getElementById("noSongsMessage");
  const audioPlayer = document.getElementById("audioPlayer");
  const playBtn = document.getElementById("playBtn");
  const playIcon = document.getElementById("playIcon");
  const playerTitle = document.getElementById("playerTitle");
  const playerArtist = document.getElementById("playerArtist");

  // Seeker & Timestamp elements
  const seeker = document.getElementById("seeker");
  const currentTimeEl = document.getElementById("currentTime");
  const durationTimeEl = document.getElementById("durationTime");

  // Format seconds to standard MM:SS display
  function formatTime(seconds) {
    if (isNaN(seconds) || !isFinite(seconds)) return "0:00";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  }

  // Render music list
  function renderSongs() {
    if (!songListEl) return;
    songListEl.innerHTML = "";

    const filtered = processedSongs.filter(
      (song) => currentFilter === "All" || song.genre === currentFilter
    );

    if (filtered.length === 0) {
      if (noSongsMsg) noSongsMsg.classList.remove("hidden");
      return;
    }

    if (noSongsMsg) noSongsMsg.classList.add("hidden");

    filtered.forEach((song) => {
      const li = document.createElement("li");
      const isPlaying = currentSong && currentSong.id === song.id && !audioPlayer.paused;
      
      li.className = `song-item ${isPlaying ? "playing" : ""}`;
      li.innerHTML = `
        <img class="song-cover" src="${song.cover}" alt="${song.title}" onerror="this.src='https://via.placeholder.com/50?text=Music'">
        <div class="song-info">
          <div class="song-title">${song.title}</div>
          <div class="song-meta">${song.artist} • ${song.album || ''}</div>
        </div>
      `;

      li.addEventListener("click", () => handleSongClick(song));
      songListEl.appendChild(li);
    });
  }

  function handleSongClick(song) {
    if (currentSong && currentSong.id === song.id) {
      if (audioPlayer.paused) {
        audioPlayer.play();
        setPlayState(true);
      } else {
        audioPlayer.pause();
        setPlayState(false);
      }
      return;
    }

    currentSong = song;
    audioPlayer.src = song.src;
    
    audioPlayer.play()
      .then(() => setPlayState(true))
      .catch((err) => console.error("Playback error:", err));

    if (playerTitle) playerTitle.textContent = song.title;
    if (playerArtist) playerArtist.textContent = `${song.artist} • ${song.album || ''}`;
    
    renderSongs();
  }

  // Genre tab selection
  if (genreTabsEl) {
    genreTabsEl.addEventListener("click", (e) => {
      if (!e.target.classList.contains("genre-tab")) return;
      document.querySelectorAll(".genre-tab").forEach((tab) => tab.classList.remove("active"));
      e.target.classList.add("active");
      currentFilter = e.target.dataset.genre || e.target.textContent.trim();
      renderSongs();
    });
  }

  // Mini-player main button
  if (playBtn) {
    playBtn.addEventListener("click", () => {
      if (!audioPlayer.src) return;
      if (audioPlayer.paused) {
        audioPlayer.play();
        setPlayState(true);
      } else {
        audioPlayer.pause();
        setPlayState(false);
      }
    });
  }

  function setPlayState(isPlaying) {
    if (playIcon) {
      playIcon.className = isPlaying ? "fa-solid fa-pause" : "fa-solid fa-play";
    }
    renderSongs();
  }

  // --- SEEKER & TIMELINE EVENTS --- //

  // Load duration when track metadata is loaded
  audioPlayer.addEventListener("loadedmetadata", () => {
    if (durationTimeEl) durationTimeEl.textContent = formatTime(audioPlayer.duration);
    if (seeker) seeker.max = audioPlayer.duration;
  });

  // Track current timestamp during playback
  audioPlayer.addEventListener("timeupdate", () => {
    if (currentTimeEl) currentTimeEl.textContent = formatTime(audioPlayer.currentTime);
    if (seeker && !seeker.isDragging) {
      seeker.value = audioPlayer.currentTime;
    }
  });

  // Drag seeker handle to scrub through track
  if (seeker) {
    seeker.addEventListener("input", () => {
      seeker.isDragging = true;
      if (currentTimeEl) currentTimeEl.textContent = formatTime(seeker.value);
    });

    seeker.addEventListener("change", () => {
      audioPlayer.currentTime = seeker.value;
      seeker.isDragging = false;
    });
  }

  audioPlayer.addEventListener("ended", () => {
    setPlayState(false);
    if (seeker) seeker.value = 0;
  });

  // Initial load
  renderSongs();
});