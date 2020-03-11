'use strict';

const e = React.createElement;

class Settings extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.buildInitialStateObject(this.props)

        document.getElementById("lang").addEventListener('change', (event) => {
            this.fetchData()
        });
    }

    buildInitialStateObject(props) {
        let initial_state = {}

        var input_states = []
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
                        if (lang) {
                            properties = properties[lang]

                            if (properties === undefined) {
                                console.log("instancio properties")
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

    updateSettings() {
        fetch("http://127.0.0.1:5000/settings", {
            method: 'POST',
            body: JSON.stringify({
                    name: this.props.section_name,
                    lang: lang,
                    data: this.state
                }
            ),
            headers: {'Content-Type': 'application/json'}
        })
            .then(res => res.json())
            .then(
                (result) => {
                    console.log(result)
                },
                (error) => {
                    console.log(error)
                }
            )
    }

    render() {
        let inputs = []
        this.props.inputs.forEach(function (value, index) {
            var form_group = e('div', {'key': index},
                e(
                    'label', {
                        htmlFor: value.input_name,
                    }, value.placeholder),
                e(
                    'input', {
                        id: value.input_name,
                        name: value.input_name,
                        type: 'text',
                        placeholder: value.placeholder,
                        value: this.state[value.input_name],
                        onChange: (e) => this.handleChange(e)
                    })
            )

            inputs.push(form_group)
        }, this)

        return (
            e('div', {style: {'marginBottom': "20px"}},
                e(
                    'h4', {},
                    this.props.section_name
                ),
                inputs,
                e(
                    'button', {
                        type: 'button',
                        onClick: (e) => this.updateSettings()
                    }, 'Actulizar'
                ),
            )
        );
    }
}

// General data form box
ReactDOM.render(
    e(Settings, {
        inputs: [
            {input_name: 'hashtag', placeholder: 'hashtag'}
        ],
        section_name: "general"
    }),
    document.querySelector('.general')
);

// Opening data form box
ReactDOM.render(
    e(Settings, {
        inputs: [
            {input_name: 'text_light', placeholder: 'Text Ligth'},
            {input_name: 'text_bold', placeholder: 'Text Bold'},
            {input_name: 'background_resource', placeholder: 'Background resource'}
        ],
        section_name: "opening"
    }),
    document.querySelector('.opening')
);

// Share data form box
ReactDOM.render(
    e(Settings, {
        inputs: [
            {input_name: 'text_bold', placeholder: 'Text Bold'},
            {input_name: 'text_left', placeholder: 'Text left'},
            {input_name: 'text_right', placeholder: 'Text right'},
            {input_name: 'show_more', placeholder: 'Show more'},
        ],
        section_name: "share"
    }),
    document.querySelector('.share')
);

// Have fun data form box
ReactDOM.render(
    e(Settings, {
        inputs: [
            {input_name: 'text_bold', placeholder: 'Text Bold'}
        ],
        section_name: "have_fun"
    }),
    document.querySelector('.have_fun')
);

// Comunity data form box
ReactDOM.render(
    e(Settings, {
        inputs: [
            {input_name: 'text_bold', placeholder: 'Text Bold'}
        ],
        section_name: "community"
    }),
    document.querySelector('.community')
);

// Popular data form box
ReactDOM.render(
    e(Settings, {
        inputs: [
            {input_name: 'text_bold', placeholder: 'Text Bold'}
        ],
        section_name: "popular"
    }),
    document.querySelector('.popular')
);

// Join Us data form box
ReactDOM.render(
    e(Settings, {
        inputs: [
            {input_name: 'text_bold', placeholder: 'Text Bold'},
            {input_name: 'text_light', placeholder: 'Text light'},
            {input_name: 'button_text', placeholder: 'Button text'}
        ],
        section_name: "join_us"
    }),
    document.querySelector('.join_us')
);

// Follow us data form box
ReactDOM.render(
    e(Settings, {
        inputs: [
            {input_name: 'follow_text', placeholder: 'Follow text'}
        ],
        section_name: "follow_us"
    }),
    document.querySelector('.follow_us')
);