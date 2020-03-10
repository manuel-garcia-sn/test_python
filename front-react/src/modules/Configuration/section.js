import React from "react";
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardActions from "@material-ui/core/CardActions";
import Button from "@material-ui/core/Button";
import { withSnackbar } from 'notistack';

class Section extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.buildInitialStateObject(this.props)
    }

    buildInitialStateObject(props) {
        let initial_state = {}

        props.inputs.forEach(function (value, index) {
            initial_state[value.input_name] = ''
        })

        return initial_state
    }

    handleChange(e) {
        this.setState({[e.target.name]: e.target.value});
    }

    componentDidMount() {
        this.fetchData()
    }

    fetchData() {
        fetch("http://localhost:5000/settings?name=" + this.props.section_name)
            .then(res => res.json())
            .then(
                (result) => {
                    if (result[0]) {
                        let properties = Object.assign({}, this.state, result[0]['data']);
                        let lang = this.props.lang
                        if (lang) {
                            properties = properties[lang]

                            if (properties === undefined) {
                                properties = {}
                            }
                        }

                        for (const prop in this.state) {
                            if (!properties.hasOwnProperty(prop)) {
                                properties[prop] = ''
                            }
                        }

                        this.setState(properties)
                    } else {
                        console.log("No settings found for this key => " + this.props.section_name)
                    }
                },
                (error) => {
                    console.log(error)
                }
            )
    }

    componentWillReceiveProps({lang}) {
        this.fetchData()
    }

    updateSettings() {
        fetch("http://127.0.0.1:5000/settings", {
            method: 'POST',
            body: JSON.stringify({
                    name: this.props.section_name,
                    lang: this.props.lang,
                    data: this.state
                }
            ),
            headers: {'Content-Type': 'application/json'}
        })
            .then(res => res.json())
            .then(
                (result) => {
                    this.props.enqueueSnackbar('Success.', {
                        variant: 'success',
                    })
                    console.log(result)
                },
                (error) => {
                    this.props.enqueueSnackbar('Error.' + error, {
                        variant: 'error',
                    })
                    console.log(error)
                }
            )
    }

    render() {
        let inputs = []
        this.props.inputs.forEach(function (value, index) {
            let element = <Grid item xs={12}>
                <TextField id={value.input_name}
                           name={value.input_name}
                           fullWidth
                           style={{'marginBottom': '10px'}}
                           placeholder={value.placeholder}
                           label={value.placeholder}
                           value={this.state[value.input_name]}
                           variant="outlined"
                           onChange={(e) => {
                               this.handleChange(e)
                           }}/>
            </Grid>
            inputs.push(element)
        }, this)

        return (
            <Card style={{'marginBottom': '50px'}}>
                <CardContent>
                    <Grid container >
                        <Grid item xs={6}>
                            <h3 style={{'margin-bottom': '20px'}}>Section: {this.props.section_name}</h3>
                        </Grid>
                        <Grid item xs={6}>
                            {inputs}
                        </Grid>
                    </Grid>
                </CardContent>
                <CardActions>
                    <Grid item xs={12} style={ {"text-align": "rigth"}}>
                        <Button variant="contained" color="primary" onClick={(e) => {
                            this.updateSettings(e)
                        }}>
                            Actualizar!
                        </Button>
                    </Grid>
                </CardActions>
            </Card>
        )
    }
}

export default withSnackbar(Section)