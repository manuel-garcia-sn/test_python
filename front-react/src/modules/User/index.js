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

class Users extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            search: '',
            users: [],
            page: 1,
            page_end: false,
            typingTimeout: 0
        }
    }

    componentDidMount() {
        this.fetchData()
    }

    fetchData() {
        fetch("http://localhost:5000/users?q=" + this.state.search +"&page=" + this.state.page)
            .then(res => res.json())
            .then(
                (result) => {
                    let page_end = result.length === 0
                    this.setState({'users': result, 'page_end': page_end})
                },
                (error) => {
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
                                <StyledTableCell>Name</StyledTableCell>
                                <StyledTableCell align="right">Total</StyledTableCell>
                                <StyledTableCell align="right">Enabled</StyledTableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {this.state.users.map(row => (
                                <StyledTableRow key={row.twitter_id}>
                                    <StyledTableCell align="right">{row.twitter_name}</StyledTableCell>
                                    <StyledTableCell align="right">{row.total}</StyledTableCell>
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
        path: '/users',
        component: withStyles(useStyles, {withTheme: true})(withSnackbar(Users)),
    },
    name: 'Users',
};
