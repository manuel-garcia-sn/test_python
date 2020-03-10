import React from 'react';
import {useState} from 'react';
import {BrowserRouter as Router, Route, Link} from "react-router-dom";
import logo from './logo.svg';
import './App.css';
import Grid from '@material-ui/core/Grid';
import {SnackbarProvider} from 'notistack';

import modules from './modules'; // All the parent knows is that it has modules ...

function App() {
    const [currentTab, setCurrentTab] = useState('dashboard');
    const styles = theme => ({
        root: {
            flexGrow: 1,
        },
        paper: {
            padding: theme.spacing(2),
            textAlign: 'center',
            color: theme.palette.text.secondary,
        },
    })

    return (
        <SnackbarProvider maxSnack={3}
                          preventDuplicate={true}
                          anchorOrigin={{
                              vertical: 'top',
                              horizontal: 'right',
                          }}>
            <Router>
                <div className="App">
                    <header className="App-header">
                        <img src={logo} className="App-logo" alt="logo"/>
                        <ul className="App-nav">
                            {modules.map(module => ( // with a name, and routes
                                <li key={module.name} className={currentTab === module.name ? 'active' : ''}>
                                    <Link to={module.routeProps.path}
                                          onClick={() => setCurrentTab(module.name)}>{module.name}</Link>
                                </li>
                            ))}
                        </ul>
                    </header>
                    <div className="App-content">
                        <Grid container justify={"center"}>
                            {modules.map(module => (
                                <Route {...module.routeProps} key={module.name}/>
                            ))}
                        </Grid>
                    </div>
                </div>
            </Router>
        </SnackbarProvider>

    );
}

export default App