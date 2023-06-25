import React, { useState } from 'react';
import { View, Text, TextInput, Button } from 'react-native';

const UserProfileScreen = () => {
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');

  const handleSaveProfile = () => {
    // Handle saving user profile logic here
    console.log('Saving profile...');
    console.log('Name:', name);
    console.log('Age:', age);
    console.log('Gender:', gender);
  };

  return (
    <View>
      <Text>User Profile</Text>
      <TextInput
        placeholder="Name"
        value={name}
        onChangeText={setName}
      />
      <TextInput
        placeholder="Age"
        value={age}
        onChangeText={setAge}
        keyboardType="numeric"
      />
      <TextInput
        placeholder="Gender"
        value={gender}
        onChangeText={setGender}
      />
      <Button title="Save Profile" onPress={handleSaveProfile} />
    </View>
  );
};

export default UserProfileScreen;
