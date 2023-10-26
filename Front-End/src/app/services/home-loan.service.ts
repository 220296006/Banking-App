import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HomeLoanService {

  private apiUrl = 'http://localhost:8000'; // Update with your API endpoint

  constructor(private http: HttpClient) { }

  calculateHomeLoan(principal: number, interestRate: number, loanTerm: number, username: string): Observable<any> {
    // Define the data to send to the API
    const requestData = {
      principal,
      interest_rate: interestRate,
      loan_term: loanTerm,
      username // Include the username here
    };

    // Make an HTTP POST request to the API
    return this.http.post<any>(`${this.apiUrl}/calculate-home-loan/`, requestData);
  }

  handleError(error: HttpErrorResponse) {
    if (error.status === 0) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, body was: `, error.error);
    }
    // Return an observable with a user-facing error message.
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }
}
