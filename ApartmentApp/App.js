import HomeScreen from './screen/main/HomeScreen';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Icon} from 'react-native-paper';

import { store } from './core/redux/store';
import { Provider } from 'react-redux';
import HomeChat from './screen/ChatScreen/HomeChat';
import Chat from './screen/ChatScreen/Chat';



const Stack = createNativeStackNavigator();

const MyStack = () => {
  return (
    <Stack.Navigator >
      <Stack.Screen name='HomeScreen' component={HomeScreen} options={{ headerShown: false }} />

      <Stack.Screen name='HomeChat' component={HomeChat} options={{ headerShown: false }} />
      <Stack.Screen name='Chat' component={Chat} options={{ headerShown: false }} />
    </Stack.Navigator>
  );
}

const Tab = createBottomTabNavigator();
const MyTab = () => {
  return (
    <Tab.Navigator screenOptions={{
      tabBarHideOnKeyboard: true,
    }}>

      <Tab.Screen name="Home" component={MyStack} options={{ tabBarIcon: () => <Icon size={30} color="#1199" source="home" />, headerShown: false }} />
      <Tab.Screen name="Nhắn tin" component={ChatNavigator} options={{ headerShown: false, tabBarIcon: () => <Icon size={30} color="#1199" source="message" />, headerShown: false }} />
     
      <Tab.Screen name="Thông báo" component={HomeScreen} options={{ tabBarIcon: () => <Icon size={30} color="#1199" source="bell" />, headerShown: false }} />
    </Tab.Navigator>
  );
}

const Init = () => {

  return (
    <MyTab />
  )
}

export default function App() {
  return (
    <Provider store={store}>
      <NavigationContainer>
        <Init />
      </NavigationContainer>
    </Provider>

  );
}

