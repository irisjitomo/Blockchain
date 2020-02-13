import React, {useState, useEffect} from 'react'
import axios from 'axios'


export default function HomePage() {

    const [data, setData] = useState([]);
    // const [transactions, setTransactions] = useState([])


    useEffect(() => {   
    axios.get('http://localhost:5000/chain')
    .then(res => {
        // console.log(res.data)
        setData(res.data.chain)
        // console.log(res.data)
        console.log(res.data.chain)
    })
}, [])

data.map(lol => {
    (lol.transactions.map(lol2 => {
        console.log(lol2.amount)
    }))
})


    return(
        <div>
        <h1>Different Blockchain blocks:</h1>
        {data.map(newData => {
            return (
                <div key={newData.index}>
                    <h3>Index: {newData.index}</h3>
                    <h3>Previous Hash: {newData.previous_hash}</h3>
            <h4>Transactions: {newData.transactions.map(tranData => {
                return tranData.amount 
            })}</h4>
                </div>
            )
        })}
        </div>
    )
}

