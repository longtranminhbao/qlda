import * as React from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity, Linking } from 'react-native';
import { Card, Avatar } from 'react-native-paper';
import * as ImagePicker from 'expo-image-picker';
import { BillApis } from '../../core/APIs/BillAPIs';
import { useSelector } from 'react-redux';
import { useRoute } from '@react-navigation/native';

export default function PaymentDetailScreen({ navigation }) {
  const route = useRoute();
  const { billId, isPayed, paymentMethod } = route.params;
  const [bill, setBill] = React.useState({});
  const [paymentType, setPaymentType] = React.useState('Chuyển khoản Momo');
  const [selectedImage, setSelectedImage] = React.useState(null);

  const loadBill = async (id) => {
    try {
      const res = await BillApis.getBillById(id);
      setBill(res.data);
    } catch (error) {
      console.log(error);
    }
  };

  React.useEffect(() => {
    if (billId) loadBill(billId);
  }, [billId]);

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setSelectedImage(result.assets[0].uri);

      const formData = new FormData();
      formData.append('avatar', {
        uri: result.assets[0].uri,
        name: 'userProfile.jpg',
        type: 'image/jpeg',
      });

      try {
        await BillApis.updateProofById(billId, formData);
      } catch (error) {
        console.log('Lỗi upload:', error);
      }
    }
  };

  const openURL = async (url) => {
    const canOpen = await Linking.canOpenURL(url);
    if (canOpen) {
      await Linking.openURL(url);
    } else {
      console.error('Không thể mở URL:', url);
    }
  };

  const paymentPress = async () => {
    const res = await BillApis.paymentBill({
      price: bill?.fee?.price,
      resident_fee_id: bill?.fee?.id,
    });

    if (res.status === 200) {
      openURL(res.data.payUrl);
    }
  };

  return (
    <ScrollView style={styles.container}>
      {!isPayed && (
        <View>
          <Text style={styles.title}>Hình thức thanh toán</Text>
          <ScrollView horizontal={true} showsHorizontalScrollIndicator={false}>
            <TouchableOpacity onPress={() => setPaymentType('Momo')}>
              <Card.Title
                style={styles.card}
                title="Ví Momo"
                titleStyle={styles.cardTitle}
                subtitle="Miễn phí"
                left={() => <Avatar.Image size={40} source={require('../../assets/logo.png')} />}
              />
            </TouchableOpacity>
            <TouchableOpacity onPress={() => setPaymentType('Zalo')}>
              <Card.Title
                style={styles.card}
                title="Ví ZaloPay"
                titleStyle={styles.cardTitle}
                subtitle="Miễn phí"
                left={() => <Avatar.Image size={40} source={require('../../assets/logo.png')} />}
              />
            </TouchableOpacity>
            <TouchableOpacity onPress={() => setPaymentType('Chuyển khoản ngân hàng')}>
              <Card.Title
                style={styles.card}
                title="Chuyển khoản"
                titleStyle={styles.cardTitle}
                subtitle="Miễn phí"
                left={() => <Avatar.Image size={40} source={require('../../assets/logo.png')} />}
              />
            </TouchableOpacity>
          </ScrollView>
        </View>
      )}

      <View>
        <Text style={styles.title}>Chi tiết giao dịch</Text>
        <View style={styles.detail}>
          <View style={styles.item}>
            <Text style={styles.title}>Tên dịch vụ</Text>
            <Text style={styles.content}>{bill?.fee?.fee_name}</Text>
          </View>
          <View style={styles.item}>
            <Text style={styles.title}>Thời gian</Text>
            <Text style={styles.content}>{bill?.fee?.created_date}</Text>
          </View>
          <View style={styles.item}>
            <Text style={styles.title}>Giá</Text>
            <Text style={styles.content}>{`${bill?.fee?.price.toLocaleString('vi-VN')} đ`}</Text>
          </View>
          <View style={styles.item}>
            <Text style={styles.title}>Số lượng</Text>
            <Text style={styles.content}>{bill?.amount}</Text>
          </View>
          <View style={styles.item}>
            <Text style={styles.title}>Tạm tính</Text>
            <Text style={styles.content}>{`${bill?.fee?.price.toLocaleString('vi-VN')} đ`}</Text>
          </View>
          <View style={styles.item}>
            <Text style={styles.title}>Hình thức thanh toán</Text>
            <Text style={styles.content}>{paymentMethod}</Text>
          </View>
          {isPayed && (
            <View style={styles.item}>
              <Text style={styles.title}>Thanh toán ngày</Text>
              <Text style={styles.content}>{bill.payment_date}</Text>
            </View>
          )}
          {paymentType === 'Chuyển khoản ngân hàng' && (
            <>
              <View style={styles.item}>
                <Text style={styles.title}>Ngân hàng</Text>
                <Text style={styles.content}>Sacombank</Text>
              </View>
              <View style={styles.item}>
                <Text style={styles.title}>Số tài khoản</Text>
                <Text style={styles.content}>034285972384</Text>
              </View>
            </>
          )}
        </View>
      </View>

      {!isPayed && (
        <>
          {paymentType !== 'Chuyển khoản ngân hàng' ? (
            <TouchableOpacity onPress={paymentPress}>
              <Text style={styles.confirm}>Xác nhận</Text>
            </TouchableOpacity>
          ) : (
            <TouchableOpacity onPress={pickImage}>
              <Text style={styles.confirm}>Upload ảnh xác minh</Text>
            </TouchableOpacity>
          )}
        </>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 10,
  },
  card: {
    borderRadius: 15,
    marginRight: 10,
    backgroundColor: 'white',
  },
  cardTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: 'black',
  },
  detail: {
    marginTop: 20,
    backgroundColor: 'white',
    borderRadius: 15,
    padding: 10,
    shadowColor: 'blue',
    shadowOffset: { width: 1, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  item: {
    width: '100%',
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: 'whitesmoke',
  },
  content: {
    fontSize: 16,
    fontWeight: '700',
  },
  confirm: {
    color: 'white',
    backgroundColor: 'blue',
    textAlign: 'center',
    fontWeight: '700',
    padding: 15,
    marginTop: 25,
    borderRadius: 15,
  },
});
