import pytest
from unittest.mock import patch, MagicMock
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@patch('models.conn')
def test_root(mock_connect, client):
    mysql = mock_connect
    cursor = mysql.cursor(dictionary=True)
    cursor.fetchall.return_value = [
        {'id': 1, 'name': 'Item1', 'price': 10, 'discount': 0.1},
        {'id': 2, 'name': 'Item2', 'price': 15, 'discount': 0.3}
        ]

    response = client.get('/')

    assert response.status_code == 200
    assert cursor.fetchall.return_value == [
        {'id': 1, 'name': 'Item1', 'price': 10, 'discount': 0.1},
        {'id': 2, 'name': 'Item2', 'price': 15, 'discount': 0.3}
        ]
        
    assert b'Item1' in response.data
    assert b'10.0%' in response.data 
    assert b'Item2' in response.data
    assert b'30.0%' in response.data 


@patch('models.conn')
def test_add(mock_connect, client):
    mysql = mock_connect
    cursor = mysql.cursor(dictionary=True)
    cursor.return_value = cursor
    cursor.fetchall.return_value = [{'id': 1, 'name': 'Item1', 'price': 10, 'discount': 0.1}]

    response = client.post('/add_item', data={'id': 1, 'name': 'Item1', 'price': 10, 'discount': 0.1}, follow_redirects=True)

    assert response.status_code == 200
    assert mysql.commit.call_count == 1
    assert cursor.fetchall.return_value == [{'id': 1, 'name': 'Item1', 'price': 10, 'discount': 0.1},]
    assert b'Item1' in response.data
    assert b'10%' in response.data
    cursor.fetchall.assert_called_once



@patch('models.conn')
def test_delete(mock_connect, client):
    mysql = mock_connect
    cursor = mysql.cursor(dictionary=True)
    cursor.return_value = cursor
    cursor.fetchall.return_value = []
    response = client.post('/delete', data={'id': '1'})

    assert response.status_code == 302  
    cursor.commit.assert_called_once
    cursor.fetchall.assert_called_once 


@patch('models.conn')
def test_totals_displayed(mock_connect, client):
    mysql = mock_connect
    cursor = mock_connect.cursor(dictionary=True)
    mysql.cursor.return_value = cursor
    cursor.fetchall.return_value = [
        {'id': 1, 'name': 'Item1', 'price': 10, 'discount': 0.1},
        {'id': 2, 'name': 'Item2', 'price': 20, 'discount': 0.2},
    ]

    response = client.get('/')

    assert response.status_code == 200
    assert b'30.00' in response.data 
    assert b'25' in response.data 
    assert b'17%' in response.data 
