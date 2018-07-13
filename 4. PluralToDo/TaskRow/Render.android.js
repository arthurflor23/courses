import React from 'react';
import {Animated, Image, StyleSheet, Text, TouchableHighlight} from 'react-native';

import doneImg from '../images/done.png';
import {ALTO_2} from '../colors';

export default function (styles) {
    const doneAnimation = new Animated.ValueXY();

    const localStyle = StyleSheet.create({
        doneButton: {
            borderRadius: 5,
            padding: 5
        },
        row: {
            transform: doneAnimation.getTranslateTransform()
        }
    });

    const animatedPress = () => {
        Animated
            .spring(doneAnimation, {
            tension: 2,
            friction: 2,
            toValue: {
                x: -500,
                y: 0
            }
        })
            .start();

        setTimeout(() => {
            this.onDonePressed();
        }, 300);
    };

    return (
        <Animated.View style={[styles.container, localStyle.row]}>
            <Text style={styles.label}>{this.props.todo.task}</Text>
            <TouchableHighlight
                onPress={animatedPress}
                style={localStyle.doneButton}
                underlayColor={ALTO_2}>
                <Image source={doneImg}/>
            </TouchableHighlight>
        </Animated.View>
    );
}
