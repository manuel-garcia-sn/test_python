import React from 'react';
import {withStyles} from "@material-ui/core/styles";
import Grid from '@material-ui/core/Grid';
import Section from "./section";
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import InputLabel from '@material-ui/core/InputLabel';

const styles = theme => ({
    root: {
        minWidth: 275,
    },
    bullet: {
        display: 'inline-block',
        margin: '0 2px',
        transform: 'scale(0.8)',
    },
    title: {
        fontSize: 14,
    },
    pos: {
        marginBottom: 12,
    },
});

class Configuration extends React.Component {
    constructor(props) {
        super(props);
        this.state = {'lang': 'es'}
    }

    handleChange(e) {
        this.setState({'lang': e.target.value})
    }

    render() {
        const {classes} = this.props;

        return (
            <Grid item xs={10}>
                <h1 style={{'marginBottom': '30px'}}>Configuración de la landing</h1>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <FormControl>
                            <InputLabel id="demo-simple-select-label">Idioma</InputLabel>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                value={this.state.lang}
                                onChange={(e) => {
                                    this.handleChange(e)
                                }}
                            >
                                <MenuItem value={'es'}>Es</MenuItem>
                                <MenuItem value={'en'}>En</MenuItem>
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                        <Section
                            lang={this.state.lang}
                            section_name={"general"}
                            inputs={[{input_name: 'hashtag', placeholder: 'hashtag'}]}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <Section
                            lang={this.state.lang}
                            section_name={"opening"}
                            inputs={[
                                {input_name: 'text_light', placeholder: 'Text Ligth'},
                                {input_name: 'text_bold', placeholder: 'Text Bold'},
                                {input_name: 'background_resource', placeholder: 'Background resource'}
                            ]}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <Section
                            lang={this.state.lang}
                            section_name={"share"}
                            inputs={[
                                {input_name: 'text_bold', placeholder: 'Text Bold'},
                                {input_name: 'text_left', placeholder: 'Text left'},
                                {input_name: 'text_right', placeholder: 'Text right'},
                                {input_name: 'image', placeholder: 'Image', type: 'file'},
                                {input_name: 'show_more', placeholder: 'Show more'}

                            ]}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <Section
                            lang={this.state.lang}
                            section_name={"have_fun"}
                            inputs={[
                                {input_name: 'text_bold', placeholder: 'Text Bold'}
                            ]}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <Section
                            lang={this.state.lang}
                            section_name={"community"}
                            inputs={[
                                {input_name: 'text_bold', placeholder: 'Text Bold'}
                            ]}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <Section
                            lang={this.state.lang}
                            section_name={"popular"}
                            inputs={[
                                {input_name: 'text_bold', placeholder: 'Text Bold'}
                            ]}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <Section
                            lang={this.state.lang}
                            section_name={"join_us"}
                            inputs={[
                                {input_name: 'text_bold', placeholder: 'Text Bold'},
                                {input_name: 'text_light', placeholder: 'Text light'},
                                {input_name: 'button_text', placeholder: 'Button text'}
                            ]}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <Section
                            lang={this.state.lang}
                            section_name={"follow_us"}
                            inputs={[
                                {input_name: 'follow_text', placeholder: 'Follow text'}
                            ]}
                        />
                    </Grid>
                </Grid>
            </Grid>
        );
    }
}

export default {
    routeProps: {
        path: '/',
        exact: true,
        component: withStyles(styles, {withTheme: true})(Configuration)
    },
    name: 'Configuration',
}