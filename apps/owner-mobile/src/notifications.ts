import Constants from "expo-constants";
import * as Notifications from "expo-notifications";
import { Platform } from "react-native";

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowBanner: true,
    shouldShowList: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

export type NotificationData = { conversation_ref?: string; found_ref?: string };

export async function registerForOwnerNotifications(): Promise<string | null> {
  if (Platform.OS === "android") {
    await Notifications.setNotificationChannelAsync("found-items", {
      name: "Found items",
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      sound: "default",
    });
  }
  const permissions = await Notifications.getPermissionsAsync();
  let status = permissions.status;
  if (status !== Notifications.PermissionStatus.GRANTED) {
    status = (await Notifications.requestPermissionsAsync()).status;
  }
  if (status !== Notifications.PermissionStatus.GRANTED) return null;

  const projectId = Constants.expoConfig?.extra?.eas?.projectId ?? Constants.easConfig?.projectId;
  if (!projectId) throw new Error("EAS project ID is required for push registration");
  return (await Notifications.getExpoPushTokenAsync({ projectId })).data;
}

export function onNotificationOpened(handler: (data: NotificationData) => void): () => void {
  const subscription = Notifications.addNotificationResponseReceivedListener((response) => {
    handler(response.notification.request.content.data as NotificationData);
  });
  return () => subscription.remove();
}
