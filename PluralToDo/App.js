/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React from 'react';
import {Platform, StyleSheet, Text, View} from 'react-native';

import {ALICE_BLUE_1, MINE_SHAFT_1} from './colors';

const instructions = Platform.select({
    ios: 'Press Cmd+R to reload,\nCmd+D or shake for dev menu',
    android: 'Double tap R on your keyboard to reload,\nShake or press menu button for dev menu'
});

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: ALICE_BLUE_1
    },
    welcome: {
        fontSize: 20,
        textAlign: 'center',
        margin: 10
    },
    instructions: {
        textAlign: 'center',
        color: MINE_SHAFT_1,
        marginBottom: 5
    }
});

export default function App() {
    return (
        <View style={styles.container}>
            <Text style={styles.welcome}>
                Welcome to React Native!
            </Text>
            <Text style={styles.instructions}>
                To get started, edit App.js
            </Text>
            <Text style={styles.instructions}>
                {instructions}
            </Text>
        </View>
    );
}
