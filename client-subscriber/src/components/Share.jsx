import React, { useEffect, useRef, useState } from 'react';
import { io } from 'socket.io-client';

const ScreenShare = () => {
    const [roomCode, setRoomCode] = useState('');
    const [isSharing, setIsSharing] = useState(false);
    const [error, setError] = useState('');
    const socketRef = useRef();
    const peerRef = useRef();
    const localVideoRef = useRef();  // for the sharer's preview
    const remoteVideoRef = useRef(); // for viewers
    const otherUserRef = useRef();
    const userStreamRef = useRef();

    useEffect(() => {
        socketRef.current = io('http://localhost:8000');

        socketRef.current.on('other user', userID => {
            otherUserRef.current = userID;
            if (isSharing) {
                callUser();
            }
        });

        socketRef.current.on('user joined', userID => {
            otherUserRef.current = userID;
            if (isSharing) {  // If we're already sharing when someone joins
                callUser();
            }
        });

        socketRef.current.on('offer', handleOffer);
        socketRef.current.on('answer', handleAnswer);
        socketRef.current.on('ice-candidate', handleICECandidate);

        return () => {
            socketRef.current.disconnect();
            if (userStreamRef.current) {
                userStreamRef.current.getTracks().forEach(track => track.stop());
            }
        };
    }, []);

    const joinRoom = () => {
        if (!roomCode.trim()) {
            setError('Please enter a room code');
            return;
        }
        socketRef.current.emit('join room', roomCode);
        setError('');
    };

    const shareScreen = async () => {
        try {
            const stream = await navigator.mediaDevices.getDisplayMedia({
                video: true,
                audio: true
            });

            userStreamRef.current = stream;
            localVideoRef.current.srcObject = stream;
            setIsSharing(true);

            if (otherUserRef.current) {
                callUser();
            }

            // Handle stream end (when user clicks "Stop sharing")
            stream.getTracks()[0].onended = () => {
                stopSharing();
            };
        } catch (err) {
            setError('Failed to share screen: ' + err.message);
        }
    };

    const stopSharing = () => {
        if (userStreamRef.current) {
            userStreamRef.current.getTracks().forEach(track => track.stop());
        }
        if (peerRef.current) {
            peerRef.current.close();
        }
        localVideoRef.current.srcObject = null;
        remoteVideoRef.current.srcObject = null;
        setIsSharing(false);
    };

    const createPeer = () => {
        const peer = new RTCPeerConnection({
            iceServers: [
                { urls: 'stun:stun.stunprotocol.org' },
                { urls: 'stun:stun.l.google.com:19302' },
            ]
        });

        peer.onicecandidate = handleICECandidateEvent;
        peer.ontrack = handleTrackEvent;
        peer.onnegotiationneeded = handleNegotiationNeededEvent;

        return peer;
    };

    const callUser = async () => {
        peerRef.current = createPeer();
        userStreamRef.current.getTracks().forEach(track =>
            peerRef.current.addTrack(track, userStreamRef.current)
        );
    };

    const handleNegotiationNeededEvent = async () => {
        try {
            const offer = await peerRef.current.createOffer();
            await peerRef.current.setLocalDescription(offer);
            socketRef.current.emit('offer', {
                target: otherUserRef.current,
                caller: socketRef.current.id,
                sdp: peerRef.current.localDescription
            });
        } catch (err) {
            setError('Failed to create offer: ' + err.message);
        }
    };

    const handleOffer = async ({ sdp, caller }) => {
        otherUserRef.current = caller;
        peerRef.current = createPeer();

        try {
            await peerRef.current.setRemoteDescription(new RTCSessionDescription(sdp));
            const answer = await peerRef.current.createAnswer();
            await peerRef.current.setLocalDescription(answer);

            socketRef.current.emit('answer', {
                target: caller,
                caller: socketRef.current.id,
                sdp: peerRef.current.localDescription
            });
        } catch (err) {
            setError('Failed to handle offer: ' + err.message);
        }
    };

    const handleAnswer = ({ sdp }) => {
        peerRef.current.setRemoteDescription(new RTCSessionDescription(sdp))
            .catch(err => setError('Failed to set remote description: ' + err.message));
    };

    const handleICECandidateEvent = ({ candidate }) => {
        if (candidate) {
            socketRef.current.emit('ice-candidate', {
                target: otherUserRef.current,
                candidate,
            });
        }
    };

    const handleICECandidate = (incoming) => {
        const candidate = new RTCIceCandidate(incoming);
        peerRef.current.addIceCandidate(candidate)
            .catch(err => setError('Failed to add ICE candidate: ' + err.message));
    };

    const handleTrackEvent = (event) => {
        console.log('Received remote track:', event.streams[0]);
        remoteVideoRef.current.srcObject = event.streams[0];
    };

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <h1 style={styles.title}>Screen Sharing Room</h1>

                <div style={styles.inputGroup}>
                    <input
                        type="text"
                        value={roomCode}
                        onChange={(e) => setRoomCode(e.target.value)}
                        placeholder="Enter room code"
                        style={styles.input}
                    />
                    <button onClick={joinRoom} style={styles.button}>
                        Join Room
                    </button>
                </div>

                <div style={styles.buttonGroup}>
                    {!isSharing && (
                        <button onClick={shareScreen} style={styles.button}>
                            Share Screen
                        </button>
                    )}
                    {isSharing && (
                        <button
                            onClick={stopSharing}
                            style={{ ...styles.button, ...styles.stopButton }}
                        >
                            Stop Sharing
                        </button>
                    )}
                </div>

                {error && (
                    <div style={styles.error}>{error}</div>
                )}

                <div style={styles.videoContainer}>
                    <div style={styles.videoWrapper}>
                        <h3 style={styles.videoTitle}>Local Preview</h3>
                        <video
                            ref={localVideoRef}
                            autoPlay
                            playsInline
                            muted
                            style={styles.video}
                        />
                    </div>
                    <div style={styles.videoWrapper}>
                        <h3 style={styles.videoTitle}>Remote Stream</h3>
                        <video
                            ref={remoteVideoRef}
                            autoPlay
                            playsInline
                            style={styles.video}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

const styles = {
    container: {
        padding: '20px',
        maxWidth: '1200px',
        margin: '0 auto',
    },
    card: {
        backgroundColor: 'white',
        borderRadius: '8px',
        padding: '20px',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    },
    title: {
        fontSize: '24px',
        marginBottom: '20px',
        color: '#333',
    },
    inputGroup: {
        display: 'flex',
        gap: '10px',
        marginBottom: '20px',
    },
    input: {
        padding: '8px 12px',
        borderRadius: '4px',
        border: '1px solid #ddd',
        fontSize: '16px',
        flex: '1',
    },
    buttonGroup: {
        marginBottom: '20px',
    },
    button: {
        backgroundColor: '#0070f3',
        color: 'white',
        border: 'none',
        padding: '8px 16px',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '16px',
    },
    stopButton: {
        backgroundColor: '#dc2626',
    },
    error: {
        color: '#dc2626',
        marginBottom: '20px',
    },
    videoContainer: {
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '20px',
        marginTop: '20px',
    },
    videoWrapper: {
        width: '100%',
    },
    videoTitle: {
        fontSize: '16px',
        marginBottom: '10px',
        color: '#666',
    },
    video: {
        width: '100%',
        aspectRatio: '16/9',
        backgroundColor: '#1f2937',
        borderRadius: '4px',
    },
};

export default ScreenShare;