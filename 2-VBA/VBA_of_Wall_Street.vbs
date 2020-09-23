Sub ticker_data()

'' Loop that outputs ticker symbol
'' Loop that outputs yearly change from opening price to close price
'' Loop that outputs percent change from opening price to close price
'' Loop that outputs the total stock volume of a stock

'' Declaring variables
Dim ws As Worksheet
Dim ticker As String
Dim yearly_change As Double
Dim opening_price As Double
Dim closing_price As Double
Dim percent_change As Double
Dim total_volume As Double
Dim unique_ticker_row As Double
unique_ticker_row = 2

'' Challenge variables
Dim greatest_increase As Double
Dim greatest_decrease As Double
Dim greatest_volume As Double
Dim greatest_increase_ticker As String
Dim greatest_decrease_ticker As String
Dim greatest_volume_ticker As String

'' Column headers
Range("I1").Value = "Ticker"
Range("J1").Value = "Yearly Change"
Range("K1").Value = "Percent Change"
Range("L1").Value = "Total Stock Volume"

'' Column headers - For challenge
Range("P1").Value = "Ticker"
Range("Q1").Value = "Value"
Range("O2").Value = "Greatest % Increase"
Range("O3").Value = "Greatest % Decrease"
Range("O4").Value = "Greatest Total Volume"

'' Find the last row
lastrow = Cells(Rows.Count, 1).End(xlUp).Row

'' Setting intial opening price on first ticker
opening_price = Cells(2, 3).Value

'' Loop over worksheets in workbook
For Each ws In Sheets
'' Loop over rows in worksheet
    For i = 2 To lastrow
'' Conditional finding unique Tickers and writing them in column I
        If Cells(i + 1, 1).Value <> Cells(i, 1).Value Then
            ticker = Cells(i, 1).Value
            Cells(unique_ticker_row, 9).Value = ticker
'' Setting the close price
            closing_price = Cells(i, 6).Value
'' Calculating yearly change
            yearly_change = closing_price - opening_price
            Cells(unique_ticker_row, 10).Value = yearly_change
'' Calcuating percent change
            If (opening_price = 0 And closing_price = 0) Then
                percent_change = 0
            ElseIf (opening_price = 0 And closing_price <> 0) Then
                percent_change = 1
            Else
                percent_change = yearly_change / opening_price
                Cells(unique_ticker_row, 11).Value = percent_change
                Cells(unique_ticker_row, 11).NumberFormat = "0.00%"
            End If
'' Add Total Volume
            total_volume = Cells(i, 7).Value + total_volume
            Cells(unique_ticker_row, 12).Value = total_volume
            unique_ticker_row = unique_ticker_row + 1
            opening_price = Cells(i + 1, 3).Value
            total_volume = 0
        Else
            total_volume = total_volume + Cells(i, 7).Value
        End If
    Next i
'' Setting last row on yearly change column
    YC_lastrow = Cells(Rows.Count, 9).End(xlUp).Row

'' Conditional formatting
    For j = 2 To YC_lastrow
        If (Cells(j, 10).Value > 0 Or Cells(j, 10).Value = 0) Then
        Cells(j, 10).Interior.ColorIndex = 10
        ElseIf Cells(j, 10).Value < 0 Then
        Cells(j, 10).Interior.ColorIndex = 3
        End If
    Next j

    greatest_increase = ws.Cells(2, 11)
    greatest_decrease = ws.Cells(2, 11)
    greatest_volume = ws.Cells(2, 12)

'' Finding Greatest % increase", Greatest % decrease and Greatest total volume
    For m = 2 To YC_lastrow
        If greatest_increase < Ws.Cells(m, 11) Then
            greatest_increase = Ws.Cells(m, 11)
            greatest_increase_ticker = Ws.Cells(m,9)
        End If

        If greatest_decrease > Ws.Cells(m, 11) Then
            greatest_decrease = Ws.Cells(m, 11)
            greatest_decrease_ticker = Ws.Cells(m,9)
        End If

        If greatest_volume < Ws.Cells(m, 12) Then
            greatest_volume = Ws.Cells(m, 12)
            greatest_volume_ticker = Ws.Cells(m,9)
        End If
    Next m

    Ws.Range("Q2") = greatest_increase
    Ws.Range("Q3") = greatest_decrease
    Ws.Range("Q4") = greatest_volume
    Ws.Range("P2") = greatest_increase_ticker
    Ws.Range("P3") = greatest_decrease_ticker
    Ws.Range("P4") = greatest_volume_ticker
    Ws.Range("Q2").NumberFormat = "0.00%"
    Ws.Range("Q3").NumberFormat = "0.00%"

Next ws

End Sub
