import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import jwt_decode from 'jwt-decode';
import { Observable, catchError, map, throwError } from 'rxjs';
import { HomeLoan } from '../model/home-loan';

@Injectable({
  providedIn: 'root'
})
export class HomeLoanService {

  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  calculateHomeLoan(homeLoanData: HomeLoan): Observable<HomeLoan> {
    const token = localStorage.getItem('token');
    if (!token) {
      return throwError('Token is not available');
    }
  
    let username: string;
    try {
      username = this.decodeToken(token); // Decode the token to get the username
    } catch (error) {
      return throwError('Failed to decode the token');
    }

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });

    return this.http
      .post<any>(`${this.baseUrl}/calculate-home-loan/`, { ...homeLoanData, username }, { headers })
      .pipe(
        map((result) => {
          return result;
        }),
        catchError((error) => {
          return throwError('Failed to calculate Home Loan.');
        })
      );
  }

  private decodeToken(token: string): string {
    const decodedToken: any = jwt_decode(token);
    return decodedToken.sub;
  }
}
