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
        {'id': 1, 'name': 'Item1', 'price': 13, 'discount': 0.25},
        {'id': 2, 'name': 'Item2', 'price': 15, 'discount': 0.35}
        ]

    response = client.get('/')

    assert response.status_code == 200
    assert cursor.fetchall.return_value == [
        {'id': 1, 'name': 'Item1', 'price': 13, 'discount': 0.25},
        {'id': 2, 'name': 'Item2', 'price': 15, 'discount': 0.35}
        ]
        
    assert b'Item1' in response.data
    assert b'13' in response.data
    assert b'25.0%' in response.data 
    assert b'Item2' in response.data
    assert b'15' in response.data
    assert b'35.0%' in response.data 
    assert b'19.50' in response.data 


@patch('models.conn')
def test_add(mock_connect, client):
    mysql = mock_connect
    cursor = mysql.cursor(dictionary=True)
    cursor.return_value = cursor
    cursor.fetchall.return_value = [{'id': 3, 'name': 'Item3', 'price': 25, 'discount': 0.40}]

    response = client.post('/add_item', data={'id': 3, 'name': 'Item3', 'price': 25, 'discount': 0.4}, follow_redirects=True)

    assert response.status_code == 200
    assert mysql.commit.call_count == 1
    assert cursor.fetchall.assert_called_once
    assert cursor.fetchall.return_value == [{'id': 3, 'name': 'Item3', 'price': 25, 'discount': 0.40}]
    assert b'Item3' in response.data
    assert b'25' in response.data
    assert b'40%' in response.data


@patch('models.conn')
def test_delete(mock_connect, client):
    mysql = mock_connect
    cursor = mysql.cursor(dictionary=True)
    cursor.return_value = cursor
    cursor.fetchall.return_value = [{'id': 1, 'name': 'Item1', 'price': 10, 'discount': 0.1}]

    response = client.post('/delete', data={'id': '1'})

    assert response.status_code == 302  

    assert cursor.commit.assert_called_once
    assert cursor.fetchall.call_count == 1

    assert b'Item1' not in response.data 
    assert b'10' not in response.data 
    assert b'10%' not in response.data 


@patch('models.conn')
def test_correct_totals(mock_connect, client):
    mysql = mock_connect
    cursor = mock_connect.cursor(dictionary=True)
    mysql.cursor.return_value = cursor
    cursor.fetchall.return_value = [
        {'id': 1, 'name': 'Item1', 'price': 10, 'discount': 0.1},
        {'id': 2, 'name': 'Item2', 'price': 20, 'discount': 0.2},
    ]

    response = client.get('/')

    assert response.status_code == 200
    print(response.data)
    assert b'30.00' in response.data 
    assert b'25' in response.data 
    assert b'17%' in response.data 
