import { View, Text, StyleSheet } from "react-native";

export default function LoginScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Sign In</Text>
      <Text style={styles.subtitle}>Mobile authentication — Phase 4</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#050505", alignItems: "center", justifyContent: "center" },
  title: { color: "#fafafa", fontSize: 24, fontWeight: "bold" },
  subtitle: { color: "#a1a1aa", marginTop: 8 },
});
