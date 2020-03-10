var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var e = React.createElement;

var Settings = function (_React$Component) {
    _inherits(Settings, _React$Component);

    function Settings(props) {
        _classCallCheck(this, Settings);

        var _this = _possibleConstructorReturn(this, (Settings.__proto__ || Object.getPrototypeOf(Settings)).call(this, props));

        _this.state = _this.buildInitialStateObject(_this.props);

        document.getElementById("lang").addEventListener('change', function (event) {
            _this.fetchData();
        });
        return _this;
    }

    _createClass(Settings, [{
        key: 'buildInitialStateObject',
        value: function buildInitialStateObject(props) {
            var initial_state = {};

            var input_states = [];
            props.inputs.forEach(function (value, index) {
                initial_state[value.input_name] = '';
            });

            return initial_state;
        }
    }, {
        key: 'handleChange',
        value: function handleChange(e) {
            this.setState(_defineProperty({}, e.target.name, e.target.value));
        }
    }, {
        key: 'componentDidMount',
        value: function componentDidMount() {
            this.fetchData();
        }
    }, {
        key: 'fetchData',
        value: function fetchData() {
            var _this2 = this;

            fetch("http://localhost:5000/settings?name=" + this.props.section_name).then(function (res) {
                return res.json();
            }).then(function (result) {
                if (result[0]) {
                    var properties = Object.assign({}, _this2.state, result[0]['data']);
                    if (lang) {
                        properties = properties[lang];

                        if (properties === undefined) {
                            console.log("instancio properties");
                            properties = {};
                        }
                    }

                    for (var prop in _this2.state) {
                        if (!properties.hasOwnProperty(prop)) {
                            properties[prop] = '';
                        }
                    }

                    _this2.setState(properties);
                } else {
                    console.log("No settings found for this key => " + _this2.props.section_name);
                }
            }, function (error) {
                console.log(error);
            });
        }
    }, {
        key: 'updateSettings',
        value: function updateSettings() {
            fetch("http://127.0.0.1:5000/settings", {
                method: 'POST',
                body: JSON.stringify({
                    name: this.props.section_name,
                    lang: lang,
                    data: this.state
                }),
                headers: { 'Content-Type': 'application/json' }
            }).then(function (res) {
                return res.json();
            }).then(function (result) {
                console.log(result);
            }, function (error) {
                console.log(error);
            });
        }
    }, {
        key: 'render',
        value: function render() {
            var _this4 = this;

            var inputs = [];
            this.props.inputs.forEach(function (value, index) {
                var _this3 = this;

                var form_group = e('div', { 'key': index }, e('label', {
                    htmlFor: value.input_name
                }, value.placeholder), e('input', {
                    id: value.input_name,
                    name: value.input_name,
                    type: 'text',
                    placeholder: value.placeholder,
                    value: this.state[value.input_name],
                    onChange: function onChange(e) {
                        return _this3.handleChange(e);
                    }
                }));

                inputs.push(form_group);
            }, this);

            return e('div', { style: { 'marginBottom': "20px" } }, e('h4', {}, this.props.section_name), inputs, e('button', {
                type: 'button',
                onClick: function onClick(e) {
                    return _this4.updateSettings();
                }
            }, 'Actulizar'));
        }
    }]);

    return Settings;
}(React.Component);

var domContainer = document.querySelector('.general');
ReactDOM.render(React.createElement(Settings, { inputs: [{ input_name: 'hashtag', placeholder: 'hashtag' }],
    section_name: "general" }), domContainer);

// General data form box
/*ReactDOM.render(
    e(Settings, {
        inputs: [
            {input_name: 'hashtag', placeholder: 'hashtag'}
        ],
        section_name: "general"
    }),
    document.querySelector('.general')
);*/
/*

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
);*/