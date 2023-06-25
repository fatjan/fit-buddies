import React, { useState } from 'react';
import { View, TextInput, Button } from 'react-native';
import { Input } from 'react-native-elements';

const WorkoutForm = () => {
    const [exerciseName, setExerciseName] = useState('');
    const [duration, setDuration] = useState('');
    const [intensityLevel, setIntensityLevel] = useState('');
  
    const handleSaveWorkout = () => {
      // Handle saving the workout details
      // You can perform validation and further processing here
      // For simplicity, we'll just log the values for now
      console.log('Exercise Name:', exerciseName);
      console.log('Duration:', duration);
      console.log('Intensity Level:', intensityLevel);
    };
  
    return (
      <View>
        <Input
          label="Exercise Name"
          value={exerciseName}
          onChangeText={setExerciseName}
        />
        <Input
          label="Duration"
          value={duration}
          onChangeText={setDuration}
        />
        <Input
          label="Intensity Level"
          value={intensityLevel}
          onChangeText={setIntensityLevel}
        />
        <Button title="Save Workout" onPress={handleSaveWorkout} />
      </View>
    );
  };
  