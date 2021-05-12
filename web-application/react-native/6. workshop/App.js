import React, {Component} from 'react';
import { Platform, StyleSheet, Text, View, ScrollView, TouchableOpacity, AsyncStorage } from 'react-native';

import Repo from './components/repo';
import NewRepoModal from './components/NewRepoModal';

export default class App extends Component {

  state = {
    modalVisible: false,
    repos: [{
        id: 1,
        thumbnail: 'https://avatars1.githubusercontent.com/u/6888381?v=4',
        title: 'la-capitaine-icon-theme',
        author: 'keeferrourke'
      },{
        id: 2,
        thumbnail: 'https://avatars0.githubusercontent.com/u/3171503?v=4',
        title: 'Ionic',
        author: 'ionic-team'
      },
    ]
  }

  _addRepository = async (newRepoText) => {
    const repoCall = await fetch(`http://api.github.com/repos/${newRepoText}`)
    const reponse = await repoCall.json();

    const repository = {
      id: reponse.id,
      thumbnail: reponse.owner.avatar_url,
      title: reponse.name,
      author: reponse.owner.login,
    }

    this.setState({
      modalVisible: false,
      repos: [
        ...this.state.repos,
        repository,
      ],
    });

    await AsyncStorage.setItem('@workshop:repos', JSON.stringify(this.state.repos));
  };

  async componentDidMount() {
    const repos = JSON.parse(await AsyncStorage.getItem('@workshop:repos'));
    this.setState({repos: repos ? repos : this.state.repos});
  }

  render() {
    return (
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.headerText}>Minicurso RocketSeat!</Text>
          <TouchableOpacity onPress={ () => {this.setState({ modalVisible: true }) }}>
            <Text style={styles.headerButton}>+</Text>
          </TouchableOpacity>
        </View>

        <ScrollView contentContainerStyle={styles.repoList}>
          { 
            this.state.repos.map((item) => { 
              return <Repo key={item.id} data={item} /> 
            }) 
          }
        </ScrollView>

        <NewRepoModal 
          onCancel={ () => { this.setState({modalVisible: false }) }} 
          onAdd={this._addRepository}
          visible={this.state.modalVisible} 
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#333'
  },
  header: {
    height: (Platform.OS === 'ios') ? 70 : 50,
    paddingTop: (Platform.OS === 'ios') ? 20 : 0,
    backgroundColor: '#fff',
    justifyContent: 'space-between',
    alignItems: 'center',
    flexDirection: 'row',
    paddingHorizontal: 24,
  },
  headerText: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  headerButton: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  repoList: {
    padding: 20,
  },
});
