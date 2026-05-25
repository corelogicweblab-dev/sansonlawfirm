import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Link } from "expo-router";

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.logo}>SANSON</Text>
      <Text style={styles.subtitle}>Legal OS</Text>
      <Text style={styles.tagline}>AI-Powered Legal Operating System</Text>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Mobile App — Phase 4</Text>
        <Text style={styles.cardText}>
          Full mobile experience with AI chat, document upload, case tracking,
          and realtime sync coming in Phase 4.
        </Text>
      </View>

      <Link href="/login" asChild>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>Sign In</Text>
        </TouchableOpacity>
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#050505",
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
  },
  logo: {
    fontSize: 42,
    fontWeight: "bold",
    color: "#ec4899",
    letterSpacing: 4,
  },
  subtitle: {
    fontSize: 16,
    color: "#a1a1aa",
    marginBottom: 8,
  },
  tagline: {
    fontSize: 14,
    color: "#71717a",
    marginBottom: 48,
    textAlign: "center",
  },
  card: {
    backgroundColor: "rgba(255,255,255,0.03)",
    borderRadius: 16,
    padding: 20,
    borderWidth: 1,
    borderColor: "rgba(236,72,153,0.15)",
    marginBottom: 32,
    width: "100%",
  },
  cardTitle: {
    color: "#fafafa",
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 8,
  },
  cardText: {
    color: "#a1a1aa",
    fontSize: 14,
    lineHeight: 22,
  },
  button: {
    backgroundColor: "#ec4899",
    paddingHorizontal: 32,
    paddingVertical: 14,
    borderRadius: 12,
    width: "100%",
    alignItems: "center",
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
});
