import React from 'react';
import {withStyles, makeStyles} from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TableFooter from '@material-ui/core/TableFooter';
import TablePagination from '@material-ui/core/TablePagination';
import Paper from '@material-ui/core/Paper';
import Checkbox from '@material-ui/core/Checkbox';
import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';
import IconButton from '@material-ui/core/IconButton';
import Grid from '@material-ui/core/Grid';
import { withSnackbar } from 'notistack';
import TextField from "@material-ui/core/TextField";

const StyledTableCell = withStyles(theme => ({
    head: {
        backgroundColor: theme.palette.common.black,
        color: theme.palette.common.white,
    },
    body: {
        fontSize: 14,
    },
}))(TableCell);

const StyledTableRow = withStyles(theme => ({
    root: {
        '&:nth-of-type(odd)': {
            backgroundColor: theme.palette.background.default,
        },
    },
}))(TableRow);

const useStyles = theme => ({
    table: {},
});

class Posts extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            search: 'SngularRocks',
            posts: [],
            page: 1,
            page_end: false,
            typingTimeout: 0
        }
    }

    componentDidMount() {
        this.fetchData()
    }

    fetchData() {
        fetch("http://localhost:5000/feed?q=" + this.state.search +"&page=" + this.state.page)
            .then(res => res.json())
            .then(
                (result) => {
                    let page_end = result.length === 0
                    this.setState({'posts': result, 'page_end': page_end})
                },
                (error) => {
                    console.log(error)
                }
            )
    }

    updateValidation = (e, twitter_id) => {
        let validated = e.target.checked
        console.log(e.target)
        fetch("http://localhost:5000/feed", {
            method: 'POST',
            body: JSON.stringify({
                    twitter_id: twitter_id,
                    validated: validated
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

    handleNextButtonClick = event => {
        this.setState({'page': this.state.page + 1}, this.fetchData)
    };

    handleBackButtonClick = event => {
        this.setState({'page': this.state.page - 1}, this.fetchData)
    };

    handleChange = event => {
        const self = this;

        this.setState({'search': event.target.value})

        if (self.state.typingTimeout) {
            clearTimeout(self.state.typingTimeout);
        }

        self.setState({
            'page': 1,
            'typingTimeout': setTimeout(function () {
                self.fetchData()
            }, 1000)}
        )
    };

    render() {
        const {classes} = this.props;
        return (
            <Grid item xs={10}>
                <h3>Posts module</h3>

                <TextField id='search'
                           name='search'
                           fullWidth
                           style={{'marginBottom': '10px'}}
                           placeholder='Search by hastag'
                           label='Search'
                           value={this.state.search}
                           variant="outlined"
                           onChange={(e) => {
                               this.handleChange(e)
                           }}/>

                <TableContainer component={Paper}>
                    <Table className={classes.table} aria-label="customized table">
                        <TableHead>
                            <TableRow>
                                <StyledTableCell>Text</StyledTableCell>
                                <StyledTableCell align="right">Link</StyledTableCell>
                                <StyledTableCell align="right">User</StyledTableCell>
                                <StyledTableCell align="right">Creation Date</StyledTableCell>
                                <StyledTableCell align="right">Fav</StyledTableCell>
                                <StyledTableCell align="right">RT</StyledTableCell>
                                <StyledTableCell align="right">Lang</StyledTableCell>
                                <StyledTableCell align="right">Enabled</StyledTableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {this.state.posts.map(row => (
                                <StyledTableRow key={row.twitter_id}>
                                    <StyledTableCell component="th" scope="row">
                                        {row.title}
                                    </StyledTableCell>
                                    <StyledTableCell align="right">
                                        <a href={row.link}>Ver</a>
                                    </StyledTableCell>
                                       <StyledTableCell align="right">{row.user.profile.twitter_name}</StyledTableCell>
                                    <StyledTableCell align="right">{row.created_at.$date}</StyledTableCell>
                                    <StyledTableCell align="right">{row.favorite_count}</StyledTableCell>
                                    <StyledTableCell align="right">{row.retweet_count}</StyledTableCell>
                                    <StyledTableCell align="right">{row.lang}</StyledTableCell>
                                    <StyledTableCell align="right">
                                        <Checkbox
                                            checked={row.validated}
                                            color="primary"
                                            value="primary"
                                            inputProps={{'aria-label': 'primary checkbox'}}
                                            onChange={e => { this.updateValidation(e, row.twitter_id);}}
                                        />
                                    </StyledTableCell>
                                </StyledTableRow>
                            ))}
                        </TableBody>
                        <TableFooter>
                            <TableRow>
                                <TableCell align={"right"} colSpan={5}>
                                    <IconButton onClick={this.handleBackButtonClick}
                                                disabled={this.state.page === 1}
                                                aria-label="previous page">
                                        <KeyboardArrowLeft />
                                    </IconButton>
                                    <IconButton
                                        onClick={this.handleNextButtonClick}
                                        disabled={this.state.page_end === true}
                                        aria-label="next page"
                                    >
                                        <KeyboardArrowRight/>
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        </TableFooter>
                    </Table>
                </TableContainer>
            </Grid>
        )
    }
}

export default {
    routeProps: {
        path: '/posts',
        component: withStyles(useStyles, {withTheme: true})(withSnackbar(Posts)),
    },
    name: 'Posts',
};
