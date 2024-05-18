const socket = io();
let localPeerId = null;
const peers = {}; // Store connections
const dataChannels = {}; // Store data channels
const countFilePath = 'count.txt';


socket.on('connect', () => {
  localPeerId = socket.id;
});
socket.on('connected', (message) => {
  // Display an alert or custom modal with the connection message
  alert(message); // This will show a popup with "You are connected to RantRipple"
});

// Handle receiving an offer
socket.on('offer', (data) => {
  if (data.to === localPeerId) {
    const peer = createPeerConnection(data.from);
    peer.ondatachannel = (event) => {
      const channel = event.channel;
      setupDataChannel(channel, data.from);
    };
    peer.setRemoteDescription(new RTCSessionDescription(data.offer))
      .then(() => peer.createAnswer())
      .then(answer => peer.setLocalDescription(answer))
      .then(() => {
        socket.emit('answer', { to: data.from, from: localPeerId, answer: peer.localDescription });
      });
  }
});

// Handle receiving an answer
socket.on('answer', (data) => {
  if (data.to === localPeerId) {
    const peer = peers[data.from];
    peer.setRemoteDescription(new RTCSessionDescription(data.answer));
  }
});

// Handle receiving ICE candidates
socket.on('candidate', (data) => {
  if (data.to === localPeerId) {
    const peer = peers[data.from];
    if (peer) {
      peer.addIceCandidate(new RTCIceCandidate(data.candidate));
    }
  }
});

// Handle peer disconnection
socket.on('peer-disconnected', (data) => {
  if (peers[data.peerId]) {
    peers[data.peerId].close();
    delete peers[data.peerId];
    delete dataChannels[data.peerId];
    console.log(`Peer disconnected: ${data.peerId}`);
    // Here you might want to alert other peers or update the UI
  }
});

//NEW FUNCTION 
// Function to read the count from file


function createPeerConnection(peerId) {
  const peer = new RTCPeerConnection({ iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] });
  peers[peerId] = peer;

  peer.onicecandidate = (event) => {
    if (event.candidate) {
      socket.emit('candidate', { to: peerId, from: localPeerId, candidate: event.candidate });
    }
  };

  // Create a data channel
  const dataChannel = peer.createDataChannel("dataChannel");
  setupDataChannel(dataChannel, peerId);

  peer.onconnectionstatechange = () => {
    if (peer.connectionState === 'disconnected') {
      socket.emit('peer-disconnected', { peerId: localPeerId, disconnectedPeerId: peerId });
    }
  };

  return peer;
}

function setupDataChannel(dataChannel, peerId) {
  dataChannel.onopen = () => console.log(`Data channel with ${peerId} opened`);
  dataChannel.onclose = () => console.log(`Data channel with ${peerId} closed`);
  dataChannel.onmessage = (event) => {
    console.log(`Message from ${peerId}: ${event.data}`);
    // Implement routing logic here if you receive a message meant for another peer
  };

  dataChannels[peerId] = dataChannel;
}

// Example function to send a message to a specific peer
function sendMessageToPeer(peerId, message) {
  if (dataChannels[peerId] && dataChannels[peerId].readyState === "open") {
    dataChannels[peerId].send(message);
  } else {
    console.log(`Data channel with ${peerId} is not open.`);
  }
}

// To call connectToPeer, you would need to know the peerId of the peer you're trying to connect to.
// This could be done through some form of user input or an initial discovery mechanism through the server.
const userList = document.getElementById('userList');

function addUserToList(peerId) {
    const userItem = document.createElement('li');
    userItem.textContent = `User: ${peerId}`;
    userItem.id = `user-${peerId}`;
    userList.appendChild(userItem);
}

function removeUserFromList(peerId) {
    const userItem = document.getElementById(`user-${peerId}`);
    if (userItem) {
        userList.removeChild(userItem);
    }
}

// Assuming you have a function to handle new peer connections
function handleNewPeer(peerId) {
    // Add new peer connection handling logic here
    addUserToList(peerId); // Update the UI
}

// Modify the existing peer disconnection handling logic
socket.on('peer-disconnected', (data) => {
    if (peers[data.peerId]) {
        peers[data.peerId].close();
        delete peers[data.peerId];
        delete dataChannels[data.peerId];
        console.log(`Peer disconnected: ${data.peerId}`);
        removeUserFromList(data.peerId); // Update the UI
    }
});
function createPeerConnection(peerId) {
    // Existing setup code...
    peer.oniceconnectionstatechange = () => {
      if (peer.iceConnectionState === 'connected') {
        // This is a simplistic approach; adjust according to your app's logic.
        console.log(`Connected to ${peerId}`);
        handleNewPeer(peerId); // Update the UI
      }
    };
  
    return peer;
  }
  socket.on('users-list', (users) => {
    // Clear the current list
    userList.innerHTML = '';
    updateUserList(users); // This function updates the user list UI
    document.getElementById('userCount').textContent = users.length;
  
    // Add each user to the list
    users.forEach((userId) => {
      if (userId !== socket.id) { // Optional: Exclude self from the list
        addUserToList(userId);
      }
    });
  });
  function updateUserList(users) {
    const userList = document.getElementById('userList');
    userList.innerHTML = ''; // Clear existing list
    users.forEach((userId) => {
        const userElement = document.createElement('li');
        userElement.textContent = `User: ${userId}`;
        userList.appendChild(userElement);
    });
}
function setupDataChannel(dataChannel, peerId) {
  dataChannel.onopen = () => console.log(`Data channel with ${peerId} opened`);
  dataChannel.onclose = () => console.log(`Data channel with ${peerId} closed`);
  // Add this line to integrate the chat message handling
  setupChatMessageHandler(dataChannel, peerId); // This function is defined in script2.js
  dataChannels[peerId] = dataChannel;
}
document.querySelectorAll('.external-link').forEach(link => {
  link.addEventListener('click', function(e) {
      e.preventDefault(); // Prevent the default link behavior
      const url = this.getAttribute('href');
      window.open(url, '_blank'); // Open the link in a new tab
  });
});

  