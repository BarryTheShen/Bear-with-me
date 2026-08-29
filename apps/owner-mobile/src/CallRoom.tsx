import { useEffect } from "react";
import { Button, StyleSheet, Text, View } from "react-native";
import { AudioSession, LiveKitRoom, registerGlobals } from "@livekit/react-native";

registerGlobals();

type Props = {
  serverUrl: string;
  token: string;
  onEnd: () => void;
};

export function CallRoom({ serverUrl, token, onEnd }: Props) {
  useEffect(() => {
    void AudioSession.startAudioSession();
    return () => {
      void AudioSession.stopAudioSession();
    };
  }, []);

  return (
    <LiveKitRoom serverUrl={serverUrl} token={token} connect audio={true} video={false}>
      <View style={styles.room}>
        <Text style={styles.title}>Anonymous return call</Text>
        <Text style={styles.muted}>Your phone number is not shared.</Text>
        <Button title="End call" onPress={onEnd} color="#a73c20" />
      </View>
    </LiveKitRoom>
  );
}

const styles = StyleSheet.create({
  room: { flex: 1, alignItems: "center", justifyContent: "center", gap: 12, padding: 24 },
  title: { fontSize: 24, fontWeight: "700" },
  muted: { color: "#5e6b78", marginBottom: 12 },
});
