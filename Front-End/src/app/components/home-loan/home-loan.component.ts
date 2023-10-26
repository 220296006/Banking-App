import { Component } from '@angular/core';
import { HomeLoanService } from 'src/app/services/home-loan.service';

@Component({
  selector: 'app-home-loan',
  templateUrl: './home-loan.component.html',
  styleUrls: ['./home-loan.component.css']
})
export class HomeLoanComponent {
  principal!: number;
  interestRate!: number;
  loanTerm!: number;
  homeLoanResult: any;


  constructor(private homeLoanService: HomeLoanService) {}

  calculateHomeLoan() {
    // Ensure that 'username' is assigned a value before making the request
  
      this.homeLoanService
        .calculateHomeLoan(this.principal, this.interestRate, this.loanTerm)
        .subscribe((result) => {
          this.homeLoanResult = result;
        })
    }
  }


